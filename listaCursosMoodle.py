#Author Marcelo Mazzochi Hillman
#Date 03/08/21

#Bibliotecas
import requests
import json
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

#Variaveis da URL
urlInit = 'https://YOURURL/webservice/rest/server.php?wstoken=YOUTOKEN&wsfunction='
urlEnd = '&moodlewsrestformat=json'
getAllCourses = 'core_course_get_courses'
getAllUsersCourses = 'core_enrol_get_enrolled_users'
getAllGradeUsersCourses = 'gradereport_user_get_grade_items'

#Construção da URL
url = urlInit + getAllCourses + urlEnd

#Requisição GET ignorando verificação SSL(em produção é fortemente recomendado configurar a cadeia de certificados)
response = requests.get(url, verify=False)

#armazena o JSON de retorno
dataCourses = response.json()



#Percorre a lista de cursos
for elementCourses in dataCourses:
    #Filtrar o primeiro curso que é registro padrão do Moodle
    if(elementCourses['id']==1): print("Teste Webservice")
    else:
        
        #Construção da URL
        url = urlInit + getAllUsersCourses + urlEnd

        #Requisição GET ignorando verificação SSL(em produção é fortemente recomendado configurar a cadeia de certificados)
        response = requests.get(url, params="courseid="+str(elementCourses['id']), verify=False)

        #Armazena o JSON de retorno
        dataUsersCourses = response.json()

        #print da lista de cursos com identação para facilicar visualização (Utilizamos o datetime pra converter o padrão de tempo UNIX)
        print("\n")
        print("-----------------------------------------------------------------------------------")
        print(str(elementCourses['idnumber'])+ " | " +elementCourses['shortname']+ " | " +elementCourses['fullname']+ " | " +datetime.utcfromtimestamp(elementCourses['timecreated']).strftime('%d/%m/%Y %H:%M:%S'))
        print("-----------------------------------------------------------------------------------")

        #Percorre a lista dos usuários matriculados no curso
        for elementUsersCourses in dataUsersCourses:

            #print da lista de alunos matriculados do curso
            #print(elementUsersCourses['fullname'])

            #Construção da URL
            url = urlInit + getAllGradeUsersCourses + urlEnd

            #Requisição GET ignorando verificação SSL(em produção é fortemente recomendado configurar a cadeia de certificados)
            response = requests.get(url, params="courseid="+str(elementCourses['id'])+"&userid="+str(elementUsersCourses['id']), verify=False)

            #Armazena o JSON de retorno
            dataGradeUsersCourses = response.json()

            #printa nome completo do aluno e sua nota final do curso
            print(elementUsersCourses['fullname'] + " | " + json.dumps(dataGradeUsersCourses['usergrades'][0]['gradeitems'][0]['percentageformatted']))

        print("-----------------------------------------------------------------------------------")
        print("\n")