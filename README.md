<body>

<h1>### VolumeControllerModule</h1>
<p>VolumeControllerModule software and hardware</p>

<img src="RepoImages\ArduinoSetup.jpeg" alt="ArduinoProtoboardSetupImage" width="200" >

<h1>### O Projeto ###</h1>
<p>O objetivo da ideia era controlar o volume do spotify enquanto em chamada na plataforma Discord, com isso configurei tanto o Arduino quanto o programa em Python para interpretar e executar ações com as informações dos inputs de botão e potênciometros montados de maneira simples em uma protoboard.</p>
<p>Atualmente o são tres potenciometros para controlar o volume de tres aplicativos diferentes abertos com audio ativo no computador, e um botão que simula o pressionamento da tecla "ScrollLock" no teclado usada para gerenciar o microfone na chamada do Discord, no meu caso.</p>

<h1>### Ajustes e melhorias ###</h1>
<p>O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas para as seguintes tarefas:

- Otimização do uso de processamento (uso de cpu alto demais chegando a 10% no taskManager)
- Implementar o icone do programa na barra de programas em segundo plano do windows (atualmente o encerramento do programa só pode ser feito abrindo o task manager)
- Implementar a tela LCD para interface
- Adicionar medidas de segurança para verificação de download </p>
<p></p>

<h2>## Pré-requisitos ##</h2>
<p>Antes de baixar, algumas observações e requisitos:</p>
<p>O codigo em python tem alguns prints de debug que foram mantidos, apesar de o programa nao ter nenhuma interface onde seja visivel, as etapas, principalmente da conexão com os aplicativos usam prints para localização do processo no decorrer do desenvolvimento.</p>
<p>Os aplicativos do codigo estão configurados para os mais usados com audio no meu caso (sinta-se à vontade para alterar usando a terminação correta):
        <pre>APPS = {
            0: "spotify.exe",
            1: "discord.exe",
            2: "brave.exe"
        } </pre>
Para baixar somente o executavel e ter a experiencia do modulo, o arquivo .exe esta no diretorio 'dist'
</p>
<h2>## Atente-se ##</h2>
<h3>A aplicação não se encerra sozinha, é necessario que se termine a tarefa no Gerenciador de Tarefas do windows</h3>

<p>NENHUMA MEDIDA DE SEGURANÇA PARA VERIFICAÇÃO DE DOWNLOAD FOI IMPLEMENTADA, VOCE VERÁ UM AVISO DE ARQUIVO NAO SEGURO</p>

<p>Nunca tinha escrito um codigo de Arduino, então muito desse processo tive ajuda.</p>
<p>Estou mais familiarizado com o python e essas bibliotecas usadas foram novas, entao também envolveu uma pesquisa.
O projeto esta em desenvolvimento, e será atualizado em breve.</p>

</body>