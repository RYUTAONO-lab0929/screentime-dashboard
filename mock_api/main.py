from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['*'], allow_methods=['*'])
@app.get('/v1/summary')
def summary():
    return {'week':{'labels':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],'total_hours':[3.5,3.9,4.1,4.6,4.0,4.8,4.2]}, 'category':{'labels':['教育','生産性','娯楽','SNS','その他'],'values':[2.1,1.3,0.9,0.7,0.5]}, 'kpi':{'labels':['W-5','W-4','W-3','W-2','W-1','W'],'total_hours':[24.1,25.3,26.9,27.4,28.0,29.7],'notifications':[420,460,510,495,505,540]}}
@app.get('/v1/top-apps')
def top_apps():
    return {'items':[{'app':'Safari','category':'生産性','total':'6h 05m'},{'app':'Notability','category':'教育','total':'5h 12m'},{'app':'YouTube','category':'娯楽','total':'3h 40m'},{'app':'GoodNotes','category':'教育','total':'3h 05m'},{'app':'LINE','category':'SNS','total':'2h 10m'}]}
@app.get('/v1/top-domains')
def top_domains():
    return {'items':[{'domain':'docs.google.com','total':'2h 05m'},{'domain':'wikipedia.org','total':'1h 18m'},{'domain':'news.ycombinator.com','total':'52m'},{'domain':'qiita.com','total':'45m'},{'domain':'github.com','total':'38m'}]}
@app.get('/v1/export/daily.csv')
def export_daily():
    return "date,total_hours\n2025-09-29,4.2\n2025-09-30,4.0\n2025-10-01,4.3\n"
