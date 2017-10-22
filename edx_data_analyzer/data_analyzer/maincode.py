import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from django.contrib.staticfiles.templatetags.staticfiles import static

data= pd.read_csv('/mnt/k/edm_project/edx_data_analyzer/data_analyzer/static/data_analyzer/HMXPC13_DI_v2_5-14-14.csv')





def countries_graph():
    countries = data.groupby(by = ['final_cc_cname_DI','userid_DI'])['final_cc_cname_DI'].count().reset_index(name="count")
    countries = countries.groupby(by = ['final_cc_cname_DI'])['final_cc_cname_DI'].count().reset_index(name="count")
    countries['code'] = ['AUS','BGD','BRA','CAN','CHN','COL','EGY','FRA','DEU','GRC','IND','IDN','JPN','MEX','MAR','NGA','OAF','OEA','OEU','OME/CA','ON/CA','OOC','OSAm','OSAs','PAK','PHL','POL','PRT','RUS','ESP','UKR','GBR','USA','OTHER']

    grph = [ dict(
            type = 'choropleth',
            locations = countries['code'],
            z = countries['count'],
            text = countries['final_cc_cname_DI'],
            colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
                [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'rgb(180,180,180)',
                    width = 0.5
                ) ),
            colorbar = dict(
                autotick = False,
                tickprefix = '$',
                title = 'numberOfStudents'),
          ) ]

    layout = dict(
        title = 'Number of Students Countrywise',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection = dict(
                type = 'Mercator'
            )
        )
    )

    fig = dict( data=grph, layout=layout )
    return plotly.offline.plot(fig, validate=False,  output_type='div')


def student_category_countrywise():
    studentcategory = data.groupby(by = ['final_cc_cname_DI'])['registered','viewed','explored','certified'].sum().reset_index()
    trace1 = go.Bar(
        x=studentcategory['final_cc_cname_DI'],
        y=studentcategory['registered'],
        name='registered'
    )
    trace2 = go.Bar(
        x=studentcategory['final_cc_cname_DI'],
        y=studentcategory['viewed'],
        name='viewed'
    )
    trace3 = go.Bar(
        x=studentcategory['final_cc_cname_DI'],
        y=studentcategory['explored'],
        name='explored'
    )
    trace4 = go.Bar(
        x=studentcategory['final_cc_cname_DI'],
        y=studentcategory['certified'],
        name='certified'
    )

    grph = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        barmode='overlay'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')

def gender_countrywise():
    gender = data.groupby(by = ['final_cc_cname_DI','gender'])['userid_DI'].count().reset_index()
    gender = gender.dropna(subset=['gender'])
    female= gender[gender['gender'] == 'f'].reset_index()
    male= gender[gender['gender'] == 'm'].reset_index()
    other= gender[gender['gender'] == 'o']

    trace1 = go.Bar(
        x=female['final_cc_cname_DI'],
        y=female['userid_DI'],
        name='female'
    )
    trace2 = go.Bar(
        x=male['final_cc_cname_DI'],
        y=male['userid_DI'],
        name='male'
    )
    trace3 = go.Bar(
        x=other['final_cc_cname_DI'],
        y=other['userid_DI'],
        name='others'
    )

    grph = [trace1, trace2, trace3]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')


def education_countrywise():
    loe = data.groupby(by = ['final_cc_cname_DI','LoE_DI'])['userid_DI'].count().reset_index()
    loe = loe.dropna(subset=['LoE_DI'])
    bachelors= loe[loe['LoE_DI'] == "Bachelor's"].reset_index()
    doctorate= loe[loe['LoE_DI'] == "Doctorate"].reset_index()
    ltsecondary= loe[loe['LoE_DI'] == "Less than Secondary"].reset_index()
    masters= loe[loe['LoE_DI'] == "Master's"].reset_index()
    secondary= loe[loe['LoE_DI'] == "Secondary"].reset_index()

    trace5 = go.Bar(
        x=bachelors['final_cc_cname_DI'],
        y=bachelors['userid_DI'],
        name='Bachelors'
    )
    trace6 = go.Bar(
        x=doctorate['final_cc_cname_DI'],
        y=doctorate['userid_DI'],
        name='Doctorate'
    )
    trace7 = go.Bar(
        x=ltsecondary['final_cc_cname_DI'],
        y=ltsecondary['userid_DI'],
        name=' Less than Secondary'
    )
    trace8 = go.Bar(
        x=masters['final_cc_cname_DI'],
        y=masters['userid_DI'],
        name='Masters'
    )
    trace9 = go.Bar(
        x=secondary['final_cc_cname_DI'],
        y=secondary['userid_DI'],
        name='Secondary'
    )
    grph = [trace5, trace6, trace7, trace8, trace9]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')


def birth_countrywise():
    yob = data[['final_cc_cname_DI','YoB','userid_DI']]
    yob = yob.dropna(subset=['YoB'])
    yob['YoB'] = yob['YoB'].astype(str)
    yob['YoB'] = pd.to_numeric(yob['YoB'])
    yob['daterange'] = pd.cut(yob['YoB'], bins=[1931,1950,1970,1990,2013], labels=False)
    yob['daterange'] = yob['daterange'].astype(str)
    yob['daterange'] = [w.replace('0.0', '1931-1950') for w in yob['daterange']]
    yob['daterange'] = [w.replace('1.0', '1951-1970') for w in yob['daterange']]
    yob['daterange'] = [w.replace('2.0', '1971-1990') for w in yob['daterange']]
    yob['daterange'] = [w.replace('3.0', '1991-2013') for w in yob['daterange']]
    yob = yob.groupby(by = ['final_cc_cname_DI','daterange'])['userid_DI'].count().reset_index()
    daterange1= yob[yob['daterange'] == "1931-1950"].reset_index()
    daterange2= yob[yob['daterange'] == "1951-1970"].reset_index()
    daterange3= yob[yob['daterange'] == "1971-1990"].reset_index()
    daterange4= yob[yob['daterange'] == "1991-2013"].reset_index()

    trace6 = go.Bar(
        x=daterange1['final_cc_cname_DI'],
        y=daterange1['userid_DI'],
        name='1931-1950'
    )
    trace7 = go.Bar(
        x=daterange2['final_cc_cname_DI'],
        y=daterange2['userid_DI'],
        name=' 1951-1970'
    )
    trace8 = go.Bar(
        x=daterange3['final_cc_cname_DI'],
        y=daterange3['userid_DI'],
        name='1971-1990'
    )
    trace9 = go.Bar(
        x=daterange4['final_cc_cname_DI'],
        y=daterange4['userid_DI'],
        name='1991-2013'
    )
    grph = [trace6, trace7, trace8, trace9]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')


def course_countrywise():
    courses = data.groupby(by = ['final_cc_cname_DI','course_id'])['userid_DI'].count().reset_index()
    course1 = courses[courses['course_id'] == 'HarvardX/CB22x/2013_Spring'].reset_index()
    course2 = courses[courses['course_id'] == 'HarvardX/CS50x/2012'].reset_index()
    course3 = courses[courses['course_id'] == 'HarvardX/ER22x/2013_Spring'].reset_index()
    course4 = courses[courses['course_id'] == 'HarvardX/PH207x/2012_Fall'].reset_index()
    course5 = courses[courses['course_id'] == 'HarvardX/PH278x/2013_Spring'].reset_index()
    course6 = courses[courses['course_id'] == 'MITx/14.73x/2013_Spring'].reset_index()
    course7 = courses[courses['course_id'] == 'MITx/2.01x/2013_Spring'].reset_index()
    course8 = courses[courses['course_id'] == 'MITx/3.091x/2012_Fall'].reset_index()
    course9 = courses[courses['course_id'] == 'MITx/3.091x/2013_Spring'].reset_index()
    course10 = courses[courses['course_id'] == 'MITx/6.002x/2012_Fall'].reset_index()
    course11 = courses[courses['course_id'] == 'MITx/6.002x/2013_Spring'].reset_index()
    course12 = courses[courses['course_id'] == 'MITx/6.00x/2012_Fall'].reset_index()
    course13 = courses[courses['course_id'] == 'MITx/6.00x/2013_Spring'].reset_index()
    course14 = courses[courses['course_id'] == 'MITx/7.00x/2013_Spring'].reset_index()
    course15 = courses[courses['course_id'] == 'MITx/8.02x/2013_Spring'].reset_index()
    course16 = courses[courses['course_id'] == 'MITx/8.MReV/2013_Summer'].reset_index()

    trace1 = go.Bar(
        x=course1['final_cc_cname_DI'],
        y=course1['userid_DI'],
        name='HarvardX/CB22x/2013_Spring'
    )
    trace2 = go.Bar(
        x=course2['final_cc_cname_DI'],
        y=course2['userid_DI'],
        name='HarvardX/CS50x/2012'
    )
    trace3 = go.Bar(
        x=course3['final_cc_cname_DI'],
        y=course3['userid_DI'],
        name='HarvardX/ER22x/2013_Spring'
    )
    trace4 = go.Bar(
        x=course4['final_cc_cname_DI'],
        y=course4['userid_DI'],
        name='HarvardX/PH207x/2012_Fall'
    )

    trace5 = go.Bar(
        x=course5['final_cc_cname_DI'],
        y=course5['userid_DI'],
        name='HarvardX/PH278x/2013_Spring'
    )

    trace6 = go.Bar(
        x=course6['final_cc_cname_DI'],
        y=course6['userid_DI'],
        name='MITx/14.73x/2013_Spring'
    )
    trace7 = go.Bar(
        x=course7['final_cc_cname_DI'],
        y=course7['userid_DI'],
        name='MITx/2.01x/2013_Spring'
    )
    trace8 = go.Bar(
        x=course8['final_cc_cname_DI'],
        y=course8['userid_DI'],
        name='MITx/3.091x/2012_Fall'
    )
    trace9 = go.Bar(
        x=course9['final_cc_cname_DI'],
        y=course9['userid_DI'],
        name='MITx/3.091x/2013_Spring'
    )

    trace10 = go.Bar(
        x=course10['final_cc_cname_DI'],
        y=course10['userid_DI'],
        name='MITx/6.002x/2012_Fall'
    )
    trace11 = go.Bar(
        x=course11['final_cc_cname_DI'],
        y=course11['userid_DI'],
        name='MITx/6.002x/2013_Spring'
    )
    trace12 = go.Bar(
        x=course12['final_cc_cname_DI'],
        y=course12['userid_DI'],
        name='MITx/6.00x/2012_Fall'
    )
    trace13 = go.Bar(
        x=course13['final_cc_cname_DI'],
        y=course13['userid_DI'],
        name='MITx/6.00x/2013_Spring'
    )

    trace14 = go.Bar(
        x=course14['final_cc_cname_DI'],
        y=course14['userid_DI'],
        name='MITx/7.00x/2013_Spring'
    )
    trace15 = go.Bar(
        x=course15['final_cc_cname_DI'],
        y=course15['userid_DI'],
        name='MITx/8.02x/2013_Spring'
    )
    trace16 = go.Bar(
        x=course16['final_cc_cname_DI'],
        y=course16['userid_DI'],
        name='MITx/8.MReV/2013_Summer'
    )

    grph = [trace1, trace2, trace3, trace4,trace5,trace6, trace7, trace8, trace9, trace10, trace11, trace12, trace13, trace14, trace15, trace16]
    layout = go.Layout(
        barmode='overlay'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')

def student_category_coursewise():
    studentcategory = data.groupby(by = ['course_id'])['registered','viewed','explored','certified'].sum().reset_index()

    trace1 = go.Bar(
        x=studentcategory['course_id'],
        y=studentcategory['registered'],
        name='registered'
    )
    trace2 = go.Bar(
        x=studentcategory['course_id'],
        y=studentcategory['viewed'],
        name='viewed'
    )
    trace3 = go.Bar(
        x=studentcategory['course_id'],
        y=studentcategory['explored'],
        name='explored'
    )
    trace4 = go.Bar(
        x=studentcategory['course_id'],
        y=studentcategory['certified'],
        name='certified'
    )

    grph = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        barmode='overlay'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')

def gender_coursewise():
    gender = data.groupby(by = ['course_id','gender'])['userid_DI'].count().reset_index()
    gender = gender.dropna(subset=['gender'])
    female= gender[gender['gender'] == 'f'].reset_index()
    male= gender[gender['gender'] == 'm'].reset_index()
    other= gender[gender['gender'] == 'o']

    trace1 = go.Bar(
        x=female['course_id'],
        y=female['userid_DI'],
        name='female'
    )
    trace2 = go.Bar(
        x=male['course_id'],
        y=male['userid_DI'],
        name='male'
    )
    trace3 = go.Bar(
        x=other['course_id'],
        y=other['userid_DI'],
        name='others'
    )

    grph = [trace1, trace2, trace3]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')

def education_coursewise():
    loe = data.groupby(by = ['course_id','LoE_DI'])['userid_DI'].count().reset_index()
    loe = loe.dropna(subset=['LoE_DI'])
    bachelors= loe[loe['LoE_DI'] == "Bachelor's"].reset_index()
    doctorate= loe[loe['LoE_DI'] == "Doctorate"].reset_index()
    ltsecondary= loe[loe['LoE_DI'] == "Less than Secondary"].reset_index()
    masters= loe[loe['LoE_DI'] == "Master's"].reset_index()
    secondary= loe[loe['LoE_DI'] == "Secondary"].reset_index()

    trace5 = go.Bar(
        x=bachelors['course_id'],
        y=bachelors['userid_DI'],
        name='Bachelors'
    )
    trace6 = go.Bar(
        x=doctorate['course_id'],
        y=doctorate['userid_DI'],
        name='Doctorate'
    )
    trace7 = go.Bar(
        x=ltsecondary['course_id'],
        y=ltsecondary['userid_DI'],
        name=' Less than Secondary'
    )
    trace8 = go.Bar(
        x=masters['course_id'],
        y=masters['userid_DI'],
        name='Masters'
    )
    trace9 = go.Bar(
        x=secondary['course_id'],
        y=secondary['userid_DI'],
        name='Secondary'
    )
    grph = [trace5, trace6, trace7, trace8, trace9]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')

def birth_coursewise():
    yob = data[['course_id','YoB','userid_DI']]
    yob = yob.dropna(subset=['YoB'])
    yob['YoB'] = yob['YoB'].astype(str)
    yob['YoB'] = pd.to_numeric(yob['YoB'])
    yob['daterange'] = pd.cut(yob['YoB'], bins=[1931,1950,1970,1990,2013], labels=False)
    yob['daterange'] = yob['daterange'].astype(str)
    yob['daterange'] = [w.replace('0.0', '1931-1950') for w in yob['daterange']]
    yob['daterange'] = [w.replace('1.0', '1951-1970') for w in yob['daterange']]
    yob['daterange'] = [w.replace('2.0', '1971-1990') for w in yob['daterange']]
    yob['daterange'] = [w.replace('3.0', '1991-2013') for w in yob['daterange']]
    yob = yob.groupby(by = ['course_id','daterange'])['userid_DI'].count().reset_index()
    daterange1= yob[yob['daterange'] == "1931-1950"].reset_index()
    daterange2= yob[yob['daterange'] == "1951-1970"].reset_index()
    daterange3= yob[yob['daterange'] == "1971-1990"].reset_index()
    daterange4= yob[yob['daterange'] == "1991-2013"].reset_index()

    trace6 = go.Bar(
        x=daterange1['course_id'],
        y=daterange1['userid_DI'],
        name='1931-1950'
    )
    trace7 = go.Bar(
        x=daterange2['course_id'],
        y=daterange2['userid_DI'],
        name=' 1951-1970'
    )
    trace8 = go.Bar(
        x=daterange3['course_id'],
        y=daterange3['userid_DI'],
        name='1971-1990'
    )
    trace9 = go.Bar(
        x=daterange4['course_id'],
        y=daterange4['userid_DI'],
        name='1991-2013'
    )
    grph = [trace6, trace7, trace8, trace9]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=grph, layout=layout)
    return plotly.offline.plot(fig, validate=False, output_type='div')


options = {1 : countries_graph,
           2 : student_category_countrywise,
           3 : gender_countrywise,
           4 : education_countrywise,
           5 : birth_countrywise,
           6 : course_countrywise,
           7 : student_category_coursewise,
           8 : gender_countrywise,
           9 : education_coursewise,
           10 : birth_coursewise,
}





















# def data_extract():
#     # url = static('HMXPC13_DI_v2_5-14-14.csv')
#     data= pd.read_csv('/mnt/k/edm_project/edx_data_analyzer/data_analyzer/static/data_analyzer/HMXPC13_DI_v2_5-14-14.csv')
#     trimdata = data[:1000]
#     train = data[data['grade']!='0']
#     train = data.dropna(subset = ['grade'])
#     test = data[data['grade']=='0']
#     return "Data Extracted and Split into Test and Train"
