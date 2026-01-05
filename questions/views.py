from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Question, Category
from .forms import QuestionForm, AnswerForm

# Create your views here.


def question_list(request):
    """전체 질문 목록"""
    questions = Question.objects.all()
    sort_param = request.GET.get("sort", "latest")

    if sort_param =="oldest":
        questions = questions.order_by("created_at", "id")
    else:
        questions = questions.order_by("-created_at", "-id")
    categories = Category.objects.all()
    context = {
        "questions": questions,
        "categories": categories,
        "selected_sort": sort_param,
        "selected_category":None,
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

    #화면 렌더링에 필요한 카테고리 목록
    categories = Category.objects.all()
    sort_param = request.GET.get("sort", "latest") #기본값 lagtest로 설정
    session_categories = Category.objects.filter(category_type="session").order_by("name")
    assignment_categories = Category.objects.filter(category_type="assignment").order_by("name")


 
    
    #시간순 정렬 
    if sort_param == "oldest":
        #오래된 순
        questions = questions.order_by("created_at")
    else:
        #최신순
        questions = questions.order_by("-created_at")

    
    #템플릿에 전달할 데이터 꾸러미(context)
    context = {
        "questions": questions,
        "categories": categories,
        "selected_category": category,

        #현재 선택된 필터 상태도 같이 넘겨두면 템플릿에서 선택값 유지하기 용이함
        "session_categories": session_categories,
        "assignment_categories": assignment_categories,
        "selected_sort": sort_param,
    }

    #질문 리스트 페이지 렌더링
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


def staff_unanswered(request):
    """
    [김서윤] 운영진 대시보드
    TODO: 미답변 질문 리스트 필터링 및 통계 기능 구현
    """
    # 에러 방지를 위한 기본 구현 (미해결 질문만 표시)
    questions = Question.objects.filter(is_resolved=False)
    return render(request, "questions/staff_unanswered.html", {"questions": questions})
