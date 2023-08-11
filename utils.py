
# Define a dictionary of words replacements

replacements = {' se ': ' schneider electric ',
                'delivery dates': 'delivery date',
                'time delivery': 'delivery time',
                'delivered time': 'delivery time',
                'solved problem': 'solve problem',
                'solve problems': 'solve problem',
                'tech support': 'technical support',
                'circuit breaker': 'circuit breakers',
                'called back': 'call back',
                'lead times': 'lead time',
                'leadtime': 'lead time',
                'support service': 'service support',
                'sales representatives': 'sales representative',
                'service sales': 'sales service',
                'account managers': 'account manager',
                'power supplies': 'power supply',
                'touch panels': 'touch panel',
                'touch screens': 'touch screen',
                'frequency inverter': 'frequency inverters',
                'frequency converter': 'frequency converters',
                'servo motor': 'servo motors',
                'servomotor': 'servo motors',
                'servomotors': 'servo motors',
                'control system': 'control systems',
                'electrical component': 'electrical components',
                'control cabinet': 'control cabinets',
                'speed drive': 'speed drives',
                'push button': 'push buttons',
                'touchscreen': 'touch screen',
                'spare parts': 'spare part',
                ' plcs': ' programmable logic controller',
                ' plc': ' programmable logic controller',
                # ' apc': 'american power conversion',
                ' upss': ' uninterruptible power supply',
                'becuase': 'because',
                'xxxx': ''
                }

# Filter the countries we want to copy the original comment (those in english) in the translation column for comment
# Define the list of countries you want to update
countries_to_update = ['Australia', 'Canada', 'Egypt','India','Ireland','Kuwait','Malaysia','New Zealand','Oman','Pakistan','Qatar','Saudi Arabia','Singapore','South Africa','USA','Taiwan','United Arab Emirates','United Kingdom']
# Concatenate all comment column with english content, after renaming in AbstractDataLoader
text_data_column = ['Translation_Customer_Comments', 'Translation_Overall_Additional_Comments', 'Translation_Anything_Else_Comment', 'Translation_Reason_for_Score_Comment']
# Define a list of words to filter
words_to_filter = ['no','not','none','nil','ok','okay','ras','done','nothing','hi','all','thanks','well','everything','right','very','no problem','great','good','bad','excellent','particularly']

ngrams_list = ['schneider electric','supply chain','solve problem','lead time','price performance ratio','price quality ratio','pro face','spare part','programmable logic controller', 'uninterruptible power supply', #'american power conversion',
           'product range','product line','user friendly','data sheets','allen bradley',
           'technical support','tehnical assistance','technical team','technical service',
           'delivery time','long time','delivery date','response time','quick response',
           'customer service','customer center','customer support','contact person','service support','call center','call back',
           'sales service','sales team','account manager','pre sales','sales representative',
           'circuit breakers','frequency converters','low voltage','touch panel','frequency inverters','push buttons','electrical components','control cabinets','touch screen','control systems','servo motors','power supply','speed drives',
           'alles tip top','alles tip','sinan chalabi']

more_stopwords = ['schneider electric','se','schneider','schneiders','also','xxx','xxxx','xxxxx','ok','okk','okay','ras','na','nil','none','mr','mrs','monsieur','thank','esther','ester','paulo','paolo','sadao','carlos','pereira','ken','benoit','sergio','catalina','cesar','rufo','moraleda','ferrer','guido','smekens','castelli','muiz','roberto','matteo','guerriera','mike','elena','isabel','jurrie','javier','anna','fernandez','reyes','cichinelli','inicio','incio','jos','fabio','canedo','mituo','eduardo','roberto','santos','inicio','silva','arnaldo','sgueglia','squeglia','sandrine','laroche','lavinia','salerno','fahler','rodriguez','perez','prieto','heleni','henri','henrique','henrik','sammy','gregoire','denis','thomas','divani','flavio','rosetti','fabbri','danilo','evandro','sahil','kundli','maggico','cindy','martin','gabrielsson','edoardo','martha','ponte','aponte','pinkowitz','cortese','nicole','gahner','maulady','ahmad','heidi','okino','wang','jason','james','rhandzi','cecil','went','goes','thanks','thank','alles tip','alles tip top','66666666666666','000000000000000','666666666','eng','particular','particularly','alles']

labels = [['product','features','performance','software','framework','touch screen','touch panels','sensor','drive','servo motors','license','manual','cad','sensor','eocr','pro face','proface','atv','converter','inverter','frequency converters','tcp','modbus','vijeo','gp','control cabinet','cupboard','programmable logic controller','power supply'],
['pricing','price','offers','orders','payment','invoice','quote','quotation'],
['quality','reliability','complaint','issue','warranty','repair','maintenance','incident','fault','complication','rate','rating','inconvenient','remark','improvement','feedback'],
['delivery','delivery date','delivery time','delays','stock','shipping','lead time','deadline','package','ddt','schedule'],
['customer support','communication','customer service','assistance','support','chat','email','telephone','ticket','attendance','interlocutor','operator','help','experience','uncomfy','agility','professionalism'],
['technical support','technical','technician','guidance','intervention','competence','explanation','solve','query','inquiry','resolution','troubleshooting'],
['response time','correspondence','response','quick','answer'],
['business relation','factories','supplier','cooperation','partnership','oem','business','commercial','siemens']]