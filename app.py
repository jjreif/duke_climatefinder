import pandas as pd
import streamlit as st


@st.cache
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


def main():

    #Streamlit ux setup
    
    st.set_page_config(page_title='Duke Climate Finder', initial_sidebar_state = 'auto')
    # Hide rainbow bar
    hide_decoration_bar_style = '''
        <style>
            header {visibility: hidden;}
        </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide hamburger menu & footer
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    st.sidebar.image(image='https://upload.wikimedia.org/wikipedia/commons/e/e6/Duke_University_logo.svg',use_column_width=True)
    st.sidebar.markdown('# Duke Climate Finder')
    
    selector = st.sidebar.radio('',['Find Courses','Find Research'],index=0)

    if selector == 'Find Courses':

        data = st.file_uploader('Upload csv file of courses',type='csv', accept_multiple_files=False)
        keywords = st.text_area('Enter keywords to search (separated by commas):')
        yearoptions = ['2018','2019','2020','2021','2022']
        yearsaddall = yearoptions
        yearsaddall.append('Select all')
        years = st.multiselect('Filter by years',options=yearsaddall,default='Select all')

        if st.button('Find courses'):
            if data is not None:
                df = pd.read_csv(data,header=0)
                keywords = keywords.split(',')
                keywords = [key.strip() for key in keywords]

                if 'Select all' in years:
                    years = yearoptions
                years = list(years)
                
                # st.write(df.head())

                # Filter
                df_filtered = df.loc[df['Term Descr'].str.contains('|'.join(years),na=False)]
                df_filtered = df_filtered.loc[df_filtered['Course Long Descr'].str.contains('|'.join(keywords),na=False),:]
                csv = convert_df(df_filtered)
                st.write('Out of {} total courses, there are {} courses matching these keywords'.format(len(df),len(df_filtered)))

                st.download_button("Download filtered course list",csv,"courses.csv","text/csv",key='download-csv')

    if selector == 'Find Research':
        data = st.file_uploader('Upload data in csv file',type='csv', accept_multiple_files=False)
        if data is not None:
            df = pd.read_csv(data,header=0)
            schoolvals = list(df['Scholars School Name'].unique())
            schoolvalsaddall = schoolvals
            schoolvalsaddall.append('Select all')
            schools = st.multiselect('Filter by School',options=schoolvalsaddall,default='Select all')
            if 'Select all' in schools:
                schools = schoolvals
            # all_options = st.checkbox('Select all')
            # if all_options:
            #     schools = schoolvals
            keywords = st.text_area('Enter keywords to search (separated by commas):')

        if st.button('Find researchers'):
            keywords = keywords.split(',')
            keywords = [key.strip() for key in keywords]
            # st.write(df.head())

            # Filter
            df_filtered = df.loc[df['Scholars School Name'].str.contains('|'.join(schools),na=False)]
            df_filtered = df_filtered.loc[df['Overview Text'].str.contains('|'.join(keywords),na=False),:]
            csv = convert_df(df_filtered)
            st.write('Out of {} researchers at Duke, there are {} whose description contains one of these keywords'.format(len(df),len(df_filtered)))

            st.download_button("Download filtered list of researchers",csv,"researchers.csv","text/csv",key='download-csv')

if __name__ == '__main__':
    main()