from django.shortcuts import render
from .forms import NameForm
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def index1(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():  # 检查输入是否规范
            ans = {}
            name = form.cleaned_data['name1']
            ans['head'] = name
            return render(request, 'testapp/redirectpage.html', ans)
    else:
        return render(request, 'testapp/redirectpage.html')
