from dataclasses import dataclass
import polars as pl
import streamlit as st

from services.services import create_entity, read_all_entities, read_entity, update_entity, delete_entity, delete_table
from services.services import get_metadata, get_query, download_db, upload_luma_csv



@dataclass
class layout:

    token:str

    def __post_init__(self):

        try:
            self.tables_columns = get_metadata(self.token)
        except:
            print("Enter credentials")
        self.table_names = ["Companies", "Contacts", "Events", "Members", "Transactions", "User"]


    def create_data(self):


        table_name = st.selectbox(f"Tables", (self.table_names))
        
        st.divider()

        self.form_generator("create", self.tables_columns, table_name, "Id is autoincremented")



    def read_tab(self):
 

        with st.form("read_form"):
            left, right = st.columns(2)

            
            with left:
                table_name = st.selectbox("Välj tabell", self.table_names, index=0, placeholder="Select contact method...",)

            with right:
                parameter = st.number_input(label="Sök upp", value=None, step=1)
                optional_query = st.text_input(label="SQL query", value="")


            submitted = st.form_submit_button("Submit")
            if submitted:

                if optional_query != "" and not parameter:
                    st.data_editor(pl.DataFrame(get_query(optional_query)), key="query_df")

                if not parameter:
                    st.data_editor(pl.DataFrame(read_all_entities(table_name, self.token)), key="all_df")

                if parameter:
                    st.table(read_entity(table_name, parameter, self.token))

            else:
                st.data_editor(pl.DataFrame(read_all_entities(table_name, self.token)))



    def update_tab(self):


        left1, right1 = st.columns(2)

        with left1:
            table_name = st.selectbox(f"Tables", (self.tables_columns), key="tables")
        with right1:
            row_id = st.number_input(label="id", step=1, min_value=1)
            try:
                row_id = int(row_id)
            except ValueError as e :
                print(e)
        
        st.divider()


        self.form_generator("update", self.tables_columns, table_name, row_id)

        st.divider()

        st.markdown("### Update contacts list")

        event_description = st.text_input("Event name/description")
        uploaded_file = st.file_uploader("Choose CSV to upload")

        if uploaded_file is not None:
            #try:
            raw_df = pl.read_csv(uploaded_file)
            st.write(raw_df)

            st.write("Processed df!!!!")
            df = self.luma_to_df(raw_df, self.token)
            st.write("test")
            st.write(df)

            update_contacts = st.button("Update contacts", key="Load")
            st.write("!!!!!")
            if update_contacts:
#                upload_luma_csv(df, self.token)
                st.write("Done swizzz")
            # except Exception as e:
            #     print("Not a CSV,", e)



    def delete_tab(self):


        if 'submitted' not in st.session_state: st.session_state.submitted = False
        if 'delete_row' not in st.session_state: st.session_state.delete_row = False
        if 'delete_table' not in st.session_state: st.session_state.delete_table = False

        left, right = st.columns(2)
        
        with left:
            table_name = st.selectbox("Välj tabell", self.table_names, index=0, placeholder="Select contact method...",)

        with right:
            id = st.number_input(label="Sök upp", step=1)
        

        if st.button("Submit"): 
            st.session_state.submitted = True 


            if id != 0:
                st.session_state.delete_row = True
                df = read_entity(table_name, id, self.token)


            else:
                st.session_state.delete_table = True
                df = read_all_entities(table_name, self.token)


        if st.session_state.submitted:
            try:
                st.data_editor(df)
                st.write("Delete?")
            except UnboundLocalError as e:
                print(e)
            
            delete_btn = st.button("Delete")

            if delete_btn and id != 0: 
                deleted = delete_entity(table_name, id, self.token)
                st.session_state.delete_row == True


            elif delete_btn and id == 0: 
                deleted =  delete_table(table_name)
                st.session_state.delete_table == True

            try:

                if deleted:
                    st.write("Deleted!")
                    st.session_state.delete_row = False
                    st.session_state.submitted = False
                    st.session_state.delete_table = False
                     
            except UnboundLocalError as e:
                print(e)



    def download_tab(self):

        st.title("Backup this")

        response, backup_date = download_db(self.token)

        download = st.download_button(
            label="Download Database",
            data=response.content,
            file_name=f"{backup_date}_M10.db",
            mime="application/octet-stream"
        )

        if download:

            st.write("Databased backed up")



    def form_generator(self, CRUD: str, db_tables: dict, table: str, row_id):


        columns = db_tables[table] #column names
        new_row = {}

        with st.form(f"{CRUD} form", border=False):


            for i in range(1,len(columns)): #dynamically generate input form, from 1 to len
                
                left, right = st.columns(2)

                with left:
                    if any(keyword in columns[i] for keyword in {"price", "cost", "id", "units"}):
                        value = st.number_input(f"New {columns[i]}", key=f"{CRUD} change_{i}", step=1)

                    elif any(keyword in columns[i] for keyword in {"kg"}):
                        value = st.number_input(f"New {columns[i]}", key=f"{CRUD} change_{i}")
                        
                    else:                        
                        value = st.text_input(f"New {columns[i]}", key=f"{CRUD} change_{i}")

                new_row.update({columns[i]:value})


            if CRUD == "update":
                new_row = {feature:value for (feature, value) in new_row.items() if value != "" and value != " " }
            else:
                mock_id = table[:-1]
                new_row.update({f"{mock_id.lower()}_id":0}) #
        

            submitted = st.form_submit_button("Submit")

            if submitted:
                st.write("Successfully created:") 
                st.write(new_row)
                
                if CRUD == "update":
                    update_entity(table, row_id, new_row, self.token)
                else:
                    create_entity(table, new_row, self.token)




    def luma_to_df(self, df: pl.DataFrame, token) -> pl.DataFrame:

        nr = read_all_entities("Contacts", token)
        st.write("what is ", nr[0])


        df = df.with_columns(
            event_id = pl.lit(8),                                       # alla rader får samma
            contact_channel = pl.lit("-")        
        )

        df = df.select(["email", "name", "event_id", "contact_channel"])
        new_df = df.rename({
            "email": "contact_email", 
            "name":  "contact_name"
        })

        # old_df = pl.DataFrame(read_all_entities("Contacts", "222"))
        # existing_emails = old_df["email"].to_list()

        # df = df.filter(~pl.col("contact_email").is_in(existing_emails) )

        return new_df 



    def convert_image_to_binary(self, file):
        
        binary_data = file.read()

        return binary_data



    def convert_binary_to_image(self, blob_file, img_format=".jpg"):
        with open(f'output_image.{img_format}', 'wb') as file:
            file.write(blob_file)
