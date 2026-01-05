from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Question, Category, Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.


def question_list(request):
    """전체 질문 목록"""
    questions = Question.objects.all()
    categories = Category.objects.all()
    context = {
        "questions": questions,
        "categories": categories,
    }
    return render(request, "questions/question_list.html", context)


def question_list_by_category(request, category_id):
    """
    [이서현] 카테고리별, 과제별, 시간순 정렬 및 필터링
    TODO: 커스텀 정렬 API 및 필터링 뷰 구현
    """
    # 에러 방지를 위한 기본 구현
    category = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        "questions": questions,
        "categories": categories,
        "selected_category": category,
    }
    return render(request, "questions/question_list.html", context)


def question_detail(request, pk):
    """질문 상세 페이지"""
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    context = {
        "question": question,
        "answers": answers,
    }
    return render(request, "questions/question_detail.html", context)


def question_create(request):
    """질문 작성"""
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = None
            question.is_anonymous = True
            question.save()
            return redirect("questions:detail", pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, "questions/question_form.html", {"form": form})


def answer_create(request, pk):
    """답변 작성"""
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = None
            answer.is_anonymous = True
            answer.is_staff = False
            answer.save()

    return redirect("questions:detail", pk=pk)


def question_resolve(request, pk):
    """질문 해결 표시 토글"""
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        question.is_resolved = not question.is_resolved
        question.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"is_resolved": question.is_resolved})

        return redirect("questions:detail", pk=pk)

    return redirect("questions:detail", pk=pk)


def question_update(request, pk):
    """질문 수정"""
    question = get_object_or_404(Question, pk=pk)

    # TODO: 작성자 본인 확인 로직 필요 (if request.user != question.author: ...)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("questions:detail", pk=question.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, "questions/question_form.html", {"form": form})


def question_delete(request, pk):
    """질문 삭제"""
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        question.delete()
        return redirect("questions:list")
    return redirect("questions:detail", pk=pk)


def question_scrap(request, pk):
    """질문 찜하기 토글"""
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        # 익명 사용자도 세션 기반으로 처리 가능하도록
        # TODO: 로그인 구현되면 request.user 사용
        # 현재는 간단히 전체 카운트만 증가/감소

        # 임시: 세션 기반 찜하기
        scrapped = request.session.get(f'scrapped_{pk}', False)
        request.session[f'scrapped_{pk}'] = not scrapped

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "scrapped": not scrapped,
                "scrap_count": question.scraps.count()
            })

        return redirect("questions:detail", pk=pk)

    return redirect("questions:detail", pk=pk)


def reply_create(request, pk, answer_pk):
    """꼬리질문(답변에 대한 대댓글) 작성"""
    question = get_object_or_404(Question, pk=pk)
    parent_answer = get_object_or_404(Answer, pk=answer_pk)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.question = question
            reply.parent = parent_answer
            reply.author = None
            reply.is_anonymous = True
            reply.is_staff = False
            reply.save()

    return redirect("questions:detail", pk=pk)


def staff_unanswered(request):
    """
    [김서윤] 운영진 대시보드
    TODO: 미답변 질문 리스트 필터링 및 통계 기능 구현
    """
    # 에러 방지를 위한 기본 구현 (미해결 질문만 표시)
    questions = Question.objects.filter(is_resolved=False)
    return render(request, "questions/staff_unanswered.html", {"questions": questions})
