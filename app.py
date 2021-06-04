import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

def app():        
    df=pd.read_csv('Iris.csv')
    df.index=list(range(1,len(df)+1))
    copy=df.copy()

    st.title('Data set')
    starting_row=st.selectbox('starting row number',list(range(1,len(df)+1)))
    ending_row=st.selectbox('ending row number',list(range(starting_row,len(df)+1)))
        
    columns=st.multiselect('Choose columns',list(df.columns))
    if columns!=[]:
        copy=df[columns]
    st.dataframe(copy[starting_row-1:ending_row])
     
    flower=st.selectbox('Flower',list(pd.DataFrame(df.Species.value_counts()).index))
    st.write(f'Number of {flower} is : '+str(len(df.loc[df['Species']==flower])))
    chosen_flower=df.loc[df['Species']==flower]
    
    chosen_property=st.selectbox(f'What you want to know about {flower}',['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm'])

    Maximum=np.max(chosen_flower[chosen_property])
    Minimum=np.min(chosen_flower[chosen_property])
    Mean=np.mean(chosen_flower[chosen_property])
    Median=np.median(chosen_flower[chosen_property])
    Mode=chosen_flower[chosen_property].mode()

    if st.checkbox('Show properties'):
        
        selected=st.multiselect('Choose property',['Maximum '+chosen_property,'Minimum '+chosen_property,'Mean of '+chosen_property,'Median of '+chosen_property,'Mode of '+chosen_property])
        index=0
        for x in selected:
            extract=selected[index].split()
            if extract[0]!='Mode':
                st.write(selected[index]+':'+str(eval(extract[0])))   
            else:
                if len(list(Mode))==len(chosen_flower[chosen_property]):
                    st.write(selected[index]+':'+'No common value')
                else:
                    st.write(selected[index]+':'+str(list(Mode)))
            index+=1

    st.title('Visualization using graphs')
    plot=st.selectbox('Choose your Plot',['barplot','violinplot','boxplot','scatterplot','lineplot','swarmplot','kdeplot','hexplot','regplot','heatmap','pairplot'])
    
    st.set_option('deprecation.showPyplotGlobalUse',False)
    
    graph=df
    graph.drop('Id',axis=1,inplace=True)
    x_list=list(graph.columns)
    y_list=list(graph.columns)
   
    show_bar=True
    
    if plot=='hexplot' or plot=='kdeplot' or plot=='regplot':
        x_list.remove('Species')
        y_list.remove('Species')
        show_bar=False
        number_of_rows=len(df)
    
    st.sidebar.header('Additional customizations')
    if plot!='heatmap':
        height=st.sidebar.selectbox("Height",list(range(5,11)))
    if plot!='pairplot' and plot!='heatmap':
        x_axis=st.selectbox('Choose x axis',x_list)
        if plot=='lineplot' or x_axis=='Species':
            y_list.remove('Species')
        y_axis=st.selectbox('Choose y axis',y_list)
        if show_bar:
            number_of_rows=st.slider('choose number of rows',1,len(df))
        
        hue=None
        color=None
        if plot=='barplot' or plot=='violinplot' or plot=='boxplot' or plot=='swarmplot' or plot=='scatterplot' or plot=='lineplot':
            hue=st.sidebar.selectbox("Hue",[None]+list(graph.columns))
        if hue==None:
            color=st.sidebar.selectbox('Color',[None]+['red','blue','orange','green','black','yellow','indigo','violet','pink','grey'])
    
    if plot=='pairplot':
        hue=st.sidebar.selectbox("Hue",[None]+list(graph.columns))
    if plot=='heatmap':
        linewidth=st.sidebar.selectbox('Linewidth',list(range(6)))
        linecolor=st.sidebar.selectbox('Linecolor',[None]+['red','blue','orange','green','black','yellow','indigo','violet','pink','grey'])
        calculate=st.sidebar.selectbox('choose',[None]+['correlation','covariance'])
    
    if st.button('Plot'):
        p=plot.split('plot')
        if p[0]=='bar' or p[0]=='violin' or p[0]=='box' or p[0]=='swarm':
            sns.catplot(x=x_axis,y=y_axis,data=graph.head(number_of_rows),kind=p[0],hue=hue,height=height,color=color)
            plt.xticks(rotation=90)
        elif p[0]=='scatter' or p[0]=='line':
            sns.relplot(x=x_axis,y=y_axis,data=graph.head(number_of_rows),kind=p[0],hue=hue,height=height,color=color)
        elif p[0]=='hex' or p[0]=='kde' or p[0]=='reg':
            sns.jointplot(x=x_axis,y=y_axis,data=graph,kind=p[0],height=height,color=color)
        elif p[0]=='pair':
            sns.pairplot(df,height=height,hue=hue)
        elif p[0]=='heatmap':
            if calculate=='covariance':
                sns.heatmap(df.cov(),linewidth=linewidth,linecolor=linecolor)
            elif calculate=='correlation':
                sns.heatmap(df.corr(),linewidth=linewidth,linecolor=linecolor)
            else:
                d=df.drop('Species',axis=1)
                sns.heatmap(d,linewidth=linewidth,linecolor=linecolor)
        st.pyplot()
app()
