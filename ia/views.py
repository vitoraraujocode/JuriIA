from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from usuarios.models import Cliente
from .models import Pergunta, ContextRag
from django.http import JsonResponse, StreamingHttpResponse
from .agents import JuriAi, SecretariaAI
from typing import Iterator
from agno.agent import RunOutputEvent, RunEvent
from .models import AnaliseJurisprudencia, Documentos
from agno.agent import RunOutput
from .wrapper_evolution_api import SendMessage
from django.shortcuts import get_object_or_404
from .agents import JuriAi
from typing import Iterator
from agno.agent import RunOutputEvent, RunEvent
from django.http import StreamingHttpResponse


# Create your views here.
@csrf_exempt
def chat(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'chat.html', {'cliente': cliente})
    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        pergunta_model = Pergunta(pergunta=pergunta, cliente=cliente)
        pergunta_model.save()
        return JsonResponse({'id': pergunta_model.id})


@csrf_exempt
def stream_resposta(request):
    id_pergunta = request.POST.get('id_pergunta')

    pergunta = get_object_or_404(Pergunta, id=id_pergunta)

    def gerar_resposta():
        
        agent = JuriAi.build_agent(knowledge_filters={'cliente_id': pergunta.cliente.id})
        
        stream: Iterator[RunOutputEvent] = agent.run(pergunta.pergunta, stream=True, stream_events=True)
        for chunk in stream:
            if chunk.event == RunEvent.run_content:
                yield str(chunk.content)

    response = StreamingHttpResponse(
        gerar_resposta(),
        content_type='text/plain; charset=utf-8'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    
    return response

