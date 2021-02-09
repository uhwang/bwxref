number_of_ot_books = 39
number_of_nt_books = 27
number_of_bible_books = 66

book_to_num_xref = {}
book_to_num_export = {}

xref_type = ['BW-XRef', 'BW-Export']

def get_xref_type_bwxref(): return xref_type[0]
def get_xref_type_bwexport(): return xref_type[1]

korean_bible_name = [
    "개역개정",
    "개역한글",
    "개역개정-국한문",
    "공동번역개정",
    "바른성경",
    "새번역",
    "쉬운성경",
    "우리말성경",
    "카톨릭성경",
    "킹제임스흠정역",
    "한글킹제임스",
    "현대어성경",
    "현대인성경",
]

english_bible_name = [
    'ESV' , # English Standard Version
    'GNT' , # Good News Translation
    'HCSB', # Holman Christian Standard bible
    'ISV' , # International Standard Version
    'KJV' , # King James Version
    'MSG' , # Message Version
    'NAS1995', # New American Standard Bible
    'NIV1984', # New Internation Version (as literal as possible)
               # NIV 2011 adopted neuteral vocabularies and changed grammatical
               # inconsistency such as the mismatch of a subject(sing/plr) and verb
    'NKJV', # New King James Version
    'NLT' , # New Living Translation
    'NRSV', # New Revised Standard Version (liberal)
    'YLT' , # Young's Literal Translation
]

hebgrk_bible_name = 'BHSSBL.bdb'

# KEY  KBIB BW-INTERNAL KBIB             EBIB               BW-EXPORT 
#      ABBR    NAME     NAME             NAME               NAME 
table = {
'01': ['창'  , 'Gen' , '창세기'        , 'Genesis'        , 'Gen.'    ],
'02': ['출'  , 'Exo' , '출애굽기'      , 'Exodus'         , 'Exod.'   ],
'03': ['레'  , 'Lev' , '레위기'        , 'Leviticus'      , 'Lev.'    ],
'04': ['민'  , 'Num' , '민수기'        , 'Numbers'        , 'Num.'    ],
'05': ['신'  , 'Deu' , '신명기'        , 'Deuteronomy'    , 'Deut.'   ],
'06': ['수'  , 'Jos' , '여호수아'      , 'Joshua'         , 'Jos.'    ],
'07': ['삿'  , 'Jdg' , '사사기'        , 'Judges'         , 'Jdg.'    ],
'08': ['룻'  , 'Rut' , '룻기'          , 'Ruth'           , 'Ruth'    ],
'09': ['삼상', '1Sa' , '사무엘상'      , '1 Samuel'       , '1 Sam.'  ],
'10': ['삼하', '2Sa' , '사무엘하'      , '2 Samuel'       , '2 Sam.'  ],
'11': ['왕상', '1Ki' , '열왕기상'      , '1 Kings'        , '1 Ki.'   ],
'12': ['왕하', '2Ki' , '열왕기하'      , '2 Kings'        , '2 Ki.'   ],
'13': ['대상', '1Ch' , '역대상'        , '1 Chronicles'   , '1 Chr.'  ],
'14': ['대하', '2Ch' , '역대하'        , '2 Chronicles'   , '2 Chr.'  ],
'15': ['스'  , 'Ezr' , '에스라'        , 'Ezra'           , 'Ezr.'    ],
'16': ['느'  , 'Neh' , '느헤미야'      , 'Nehemiah'       , 'Neh.'    ],
'17': ['에'  , 'Est' , '에스더'        , 'Esther'         , 'Est.'    ],
'18': ['욥'  , 'Job' , '욥기'          , 'Job'            , 'Job'     ],
'19': ['시'  , 'Psa' , '시편'          , 'Psalms'         , 'Ps.'     ],
'20': ['잠'  , 'Pro' , '잠언'          , 'Proverbs'       , 'Prov.'   ],
'21': ['전'  , 'Ecc' , '전도서'        , 'Ecclesiastes'   , 'Eccl.'   ],
'22': ['아'  , 'Sol' , '아가'          , 'Song of Solomon', 'Cant.'   ],
'23': ['사'  , 'Isa' , '이사야'        , 'Isaiah'         , 'Isa.'    ],
'24': ['렘'  , 'Jer' , '예레미야'      , 'Jeremiah'       , 'Jer.'    ],
'25': ['애'  , 'Lam' , '예레미야애가'  , 'Lamentations'   , 'Lam.'    ],
'26': ['겔'  , 'Eze' , '에스겔'        , 'Ezekiel'        , 'Ezek.'   ],
'27': ['단'  , 'Dan' , '다니엘'        , 'Daniel'         , 'Dan.'    ],
'28': ['호'  , 'Hos' , '호세아'        , 'Hosea'          , 'Hos.'    ],
'29': ['욜'  , 'Joe' , '요엘'          , 'Joel'           , 'Joel'    ],
'30': ['암'  , 'Amo' , '아모스'        , 'Amos'           , 'Amos'    ],
'31': ['옵'  , 'Oba' , '오바댜'        , 'Obadiah'        , 'Obad.'   ],
'32': ['욘'  , 'Jon' , '요나'          , 'Jonah'          , 'Jon.'    ],
'33': ['미'  , 'Mic' , '미가'          , 'Micah'          , 'Mic.'    ],
'34': ['나'  , 'Nah' , '나훔'          , 'Nahum'          , 'Nah.'    ],
'35': ['합'  , 'Hab' , '하박국'        , 'Habakkuk'       , 'Hab.'    ],
'36': ['습'  , 'Zep' , '스바냐'        , 'Zephaniah'      , 'Zeph.'   ],
'37': ['학'  , 'Hag' , '학개'          , 'Haggai'         , 'Hag.'    ],
'38': ['슥'  , 'Zec' , '스가랴'        , 'Zechariah'      , 'Zech.'   ],
'39': ['말'  , 'Mal' , '말라기'        , 'Malachi'        , 'Mal.'    ],
'40': ['마'  , 'Mat' , '마태복음'      , 'Matthew'        , 'Matt.'   ],
'41': ['막'  , 'Mar' , '마가복음'      , 'Mark'           , 'Mk.'     ],
'42': ['누'  , 'Luk' , '누가복음'      , 'Luke'           , 'Lk.'     ],
'43': ['요'  , 'Joh' , '요한복음'      , 'John'           , 'Jn.'     ],
'44': ['행'  , 'Act' , '사도행전'      , 'Acts'           , 'Acts'    ],
'45': ['롬'  , 'Rom' , '로마서'        , 'Romans'         , 'Rom.'    ],
'46': ['고전', '1Co' , '고린도전서'    , '1Corinthians'   , '1 Co.'   ],
'47': ['고후', '2Co' , '고린도후서'    , '2Corinthians'   , '2 Co.'   ],
'48': ['갈'  , 'Gal' , '갈라디아서'    , 'Galatians'      , 'Gal.'    ],
'49': ['엡'  , 'Eph' , '에베소서'      , 'Ephesians'      , 'Eph.'    ],
'50': ['빌'  , 'Phi' , '빌립보서'      , 'Philippians'    , 'Phil.'   ],
'51': ['골'  , 'Col' , '골로새서'      , 'Colossians'     , 'Col.'    ],
'52': ['살전', '1Th' , '데살로니가전서', '1Thessalonians' , '1 Thess.'],
'53': ['살후', '2Th' , '데살로니가후서', '2Thessalonians' , '2 Thess.'],
'54': ['딤전', '1Ti' , '디모데전서'    , '1Timothy'       , '1 Tim.'  ],
'55': ['딤후', '2Ti' , '디모데후서'    , '2Timothy'       , '2 Tim.'  ],
'56': ['딛'  , 'Tit' , '디도서'        , 'Titus'          , 'Tit.'    ],
'57': ['몬'  , 'Phl' , '빌레몬서'      , 'Philemon'       , 'Phlm.'   ],
'58': ['히'  , 'Heb' , '히브리서'      , 'Hebrews'        , 'Heb.'    ],
'59': ['약'  , 'Jam' , '야고보서'      , 'James'          , 'Jas.'    ],
'60': ['벧전', '1Pe', '베드로전서'     , '1Peter'         , '1 Pet.'  ],
'61': ['벧후', '2Pe', '베드로후서'     , '2Peter'         , '2 Pet.'  ],
'62': ['요일', '1Jo', '요한1서'        , '1John'          , '1 Jn.'   ],
'63': ['요이', '2Jo', '요한2서'        , '2John'          , '2 Jn.'   ],
'64': ['요삼', '3Jo', '요한3서'        , '3John'          , '3 Jn.'   ],
'65': ['유'  , 'Jud', '유다서'         , 'Jude'           , 'Jude'    ],
'66': ['계'  , 'Rev', '요한계시록'     , 'Revelation'     , 'Rev.'    ]
}

def create_book_to_num():
    global book_to_num_xref, book_to_num_export
    
    for i in range(number_of_bible_books):
        e = table["%02d"%(i+1)]
        book_to_num_xref[e[1]] = i+1
        book_to_num_export[e[4]] = i+1
        
def get_book_num(book, type):
    global book_to_num_xref, book_to_num_export
    
    if not bool(book_to_num_xref) or not bool(book_to_num_export):
        create_book_to_num()
        
    try:
        num = book_to_num_xref[book] if type == xref_type[0] else book_to_num_export[book]
    except:
        return -1
    return num
    
    