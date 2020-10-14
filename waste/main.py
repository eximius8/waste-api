import base64
import json
import math
from pylatex import Document, Section, MiniPage, Command, Package, MultiColumn
from pylatex.table import Tabu

from pylatex.utils import bold, NoEscape
from pylatex.basic import LineBreak
from pylatex.math import Math


# gcloud functions deploy generate_waste_rep --runtime python38 --trigger-topic generate_waste_rep

class WasteReport(Document):

    def __init__(self, data):
        geometry_options = {"left": "20mm", "right": "20mm", "top": "15mm"}
        super().__init__('basic',geometry_options=geometry_options)
        
        
        data_dict = json.loads(data)

        self.name = data_dict['name']
        self.fkko = data_dict['fkko']
        self.k = data_dict['k']
        self.safety_class = data_dict['safety_class']
        self.components = data_dict['components']
        self.filename = data_dict['filename']
        self.safe_components = data_dict['safe_components']
        
       
        

        self.documentclass = Command(
                        'documentclass',
                        options=['12pt',],
                        arguments=['article'],
                    )
    def create_preamble(self):

        # packages
        self.packages.append(Package(name='fontenc', options="T2A"))
        self.packages.append(Package(name='inputenc', options="utf8"))
        self.packages.append(Package(name='babel', options="russian"))
        #self.packages.append(Package(name='tabu'))
        self.packages.append(Package(name='titlesec'))
        # preamble
        self.preamble.append(NoEscape(r"\titleformat{\section}[block]{\Large\bfseries\filcenter}{}{1em}{}"))
        self.preamble.append(NoEscape(r"\renewcommand{\arraystretch}{1.5}"))
        # bibliography
        self.preamble.append(Package('biblatex',options=['sorting=none']))
        self.preamble.append(Command('addbibresource',arguments=["sources.bib"]))
    
    def create_head(self, param, value):
        
        with self.create(MiniPage(width=r"0.27\textwidth")):
            self.append(param)
            
        with self.create(MiniPage(width=r"0.68\textwidth")):
            self.append(bold(value))   
    
    def create_comp_table(self):

        self.append(LineBreak())
        self.append(Command("scriptsize"))
        total_concp = 0
        

        with self.create(Tabu(r"|X[2]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|", to=r"\textwidth", width=8)) as data_table:
            data_table.add_hline()            
            data_table.add_row(["Компонент",
                                "Сод., \%",
                                "$C_i$",
                                "$X_i$",
                                "$Z_i$",
                                "$\lg W_i$",
                                "$W_i$",
                                "$K_i$"], 
                                #mapper=bold,
                                color="gray", escape=False)
            data_table.add_hline()
            for key, val in self.components.items():
                
              
                data_table.add_row([key, val['concp'], val['concr'], val['xi'], val['zi'], val['lgw'], val['w'], val['k'] ])
                total_concp +=float(val['concp'])
      
                data_table.add_hline()

            
            data_table.add_row(( "Компонентов учтено", str(total_concp)+" %", MultiColumn(6, align='r|', data='')))
            data_table.add_hline()    
            data_table.add_row([MultiColumn(7, align='|r|', data='Показатель К степени опасности отхода:'), self.k])
            data_table.add_hline()
            data_table.add_row(( MultiColumn(7, align='|r|', data='Класс опасности отхода:'), self.safety_class))
            data_table.add_hline()

        self.append(Command("normalsize"))
        self.append(Command("bigskip"))    
        self.append(LineBreak())

    def fill_document(self):
        """Add a section, a subsection and some text to the document."""
        self.append(Section('Протокол расчета класса опасности отхода'))
        self.create_head("Наименование отхода:", self.name)        
        self.append(Command("bigskip"))
        self.append(LineBreak()) 
        if self.fkko:
            self.create_head("Код ФККО (2020):", self.fkko)
            self.append(Command("bigskip"))
            self.append(LineBreak())
        self.append("Расчет класса опасности отхода выполнен в соответствии с \
        <<Критериями отнесения отходов к I-V классам опасности по степени негативного воздействия на окружающую среду>>, \
        утвержденными приказом МПР России от 04 декабря 2014 г. № 536.")

        self.append(Command("bigskip"))
        self.append(Command("noindent"))

        self.create_comp_table()        
        

        self.append("Показатель ")
        self.append(Math(data="K", inline=True))
        self.append(" степени опасности отхода для окружающей среды рассчитывается по следующей формуле:")
        self.append(Math(data="K=K_1+K_2+\dots +K_n,", escape=False))
        self.append("где ")
        self.append(Math(data="K_1, K_2, \ldots, K_n", inline=True, escape=False))
        self.append(NoEscape(" --- показатели степени опасности отдельных компонентов отхода для окружающей среды, "))
        
        self.append(Math(data="n ", inline=True))
        self.append(NoEscape(" --- количество компонентов отхода."))
        self.append(LineBreak())
        self.append("Отнесение отходов к классу опасности расчетным методом по показателю\
         степени опасности отхода для окружающей среды осуществляется в соответствии с таблицей:")

        self.append(LineBreak())
        self.append(Command("bigskip"))
        self.append(LineBreak())
        self.append(Command("noindent"))

        with self.create(Tabu(r"|X[c]|X[c]|", to=r"\textwidth", width=2)) as data_table:
            data_table.add_hline()            
            data_table.add_row(["Класс опасности отхода",
                                "Степень опасности 	отхода для окружающей среды"], 
                                mapper=bold,
                                color="lightgray")
            data_table.add_hline()
            data_table.add_row(["I", "$10^4 \leq  K < 10^6 $"], escape=False)
            data_table.add_hline()
            data_table.add_row(["II", "$10^3 \leq  K < 10^4 $"], escape=False)
            data_table.add_hline()
            data_table.add_row(["III", "$10^2 \leq   K  < 10^3 $"], escape=False)
            data_table.add_hline()
            data_table.add_row(["IV", "$10 \leq  K < 10^2 $"], escape=False)
            data_table.add_hline()


            data_table.add_row(["V", "$K < 10 $"], escape=False)
            data_table.add_hline()
        self.append(Command("bigskip"))
        self.append(LineBreak())

        self.append(NoEscape(r"""Степень опасности компонента отхода для окружающей среды $K_i$
        рассчитывается как отношение концентрации компонента отхода $C_i$ к коэффициенту его степени опасности для окружающей среды $W_i$:
        $$K_i = \frac{C_i}{W_i},$$
        где	$C_i$ --- концентрация $i$--тогo компонента в отходе [мг/кг]; 

        $W_i$ --- коэффициент степени опасности $i$-того компонента отхода для окружающей среды.
        """))
   
        if len(self.safe_components) == 1:
            string = f"В соответствии с компонент {self.safe_components[0]['name'].lower()} относится"

        elif len(self.safe_components) > 1:
            comps = ""
            for comp in self.safe_components[:-1]: 
                comps = comps + comp["name"] + ", " 
            comps += self.safe_components[-1]["name"]           
            string = f"В соответствии с компоненты: {comps.lower()} относятся"
        else:
            string = ""

        if string:
            self.append(NoEscape(string + r""" к практически неопасным компонентам со средним баллом 
        $X_i$, равным 4 и, следовательно, коэффициентом степени опасности для ОПС $W_i$, равным $10^6$."""))
        self.append(LineBreak())
        self.append("""Для определения коэффициента степени опасности компонента отхода \
         для окружающей среды по каждому компоненту отхода устанавливаются степени их \
         опасности для окружающей среды для различных компонентов природной среды.""")
        self.append(LineBreak())

        for name, data in self.components.items():
            if data['props']:
                self.append(LineBreak())
                self.append(f"Первичные показатели опасности компонента: {name}")
                self.append(LineBreak())
                self.print_component_data(data['props'])
        



        self.append(Command("bigskip"))
        self.generate_pdf(f'/tmp/temp{self.filename}', clean_tex=False)

    
    def print_component_data(self, props):

        with self.create(Tabu(r"|X[c]|X[c]|X[c]|X[c]|", to=r"\textwidth", width=4)) as data_table:
            data_table.add_hline()            
            data_table.add_row(["Показатель опасности",
                                "Значения показателя",
                                "Балл",
                                "Источник информации"], 
                                mapper=bold,
                                color="lightgray")
            data_table.add_hline()
            for name, value in props.items():
                data_table.add_row([name, value['value'], value['score'], value['litsource']] )
                data_table.add_hline()                              

                

        self.append(LineBreak())

        


        

       






def generate_waste_rep(context):

    # bytes_user_name = base64.b64decode(event['data'])
    # user_name = bytes_user_name.decode("utf-8") 

    doc = WasteReport(data=context)
    doc.create_preamble()
    doc.fill_document()

    

# context = { "name": "Отход 1", \
#             "fkko": "78 946 46",\
#             "safety_class": "IV", \
#             "k": "45456",
#             "components": \
#             {"кКомпонент гавностенкока фавылопаловфып выфапло фывпрвыа ыфвапрывп авфы": \
#                 {   "concp": "20", \
#                     "concr": "58", \
#                     "xi": "65", \
#                     "zi": "4564",
#                     "lgw": "1578",
#                     "w": "342",
#                     "k": "15" \
#                 }, \
#             "кКомпонент гавностенкока фавыл2": \
#                 {   "concp": "25.8", \
#                     "concr": "58", \
#                     "xi": "5789", \
#                     "zi": "4564",
#                     "lgw": "1578",
#                     "w": "342",
#                     "k": "5.5" \
#                 }, \
#             } 
#         }

# generate_waste_rep(event=0, context=json.dumps(context, ensure_ascii=False  ).encode('utf8'))

# # context='{"name": "Отход 1",\
# #  "fkko": "78 946 46",\
# #   "safety_class": "158", \
# #   "components": \
# #     "{"component1": \
# #         "{"concp": "20", \
# #           "concr": "58", \
# #           "xi": "65", \
# #           "k": "15" \
# #          }" \
# #     }" }')