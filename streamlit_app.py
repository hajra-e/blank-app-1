import streamlit as st
import pandas as pd

st.title("Dataset Cleaning App")

#CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    #dataset
    data = pd.read_csv(uploaded_file)

    # Raw data display
    st.subheader("Raw Dataset")
    st.write(data)

    # Handle Missing Values
    st.subheader("Handle Missing Values")
    
    # Replace placeholders for missing values
    missing_value_placeholder = st.text_input("Enter placeholder for missing values (e.g., ..):", value="..")
    if missing_value_placeholder:
        data.replace(missing_value_placeholder, pd.NA, inplace=True)
    
    # Missing value summary
    st.write("Missing Values per Column:")
    st.write(data.isna().sum())

    # Option to fill missing values with the row mean
    fill_option = st.radio(
        "How would you like to handle missing values?",
        ("None", "Fill missing values with row mean")
    )

    if fill_option == "Fill missing values with row mean":
        st.write("Filling missing values with row mean...")
        
        # Select only numeric columns for row mean calculation
        numeric_data = data.select_dtypes(include=['number'])
        
        #row means for numeric columns
        row_means = numeric_data.mean(axis=1)  # Calculate mean for each row in numeric columns
        
        for idx, row in data.iterrows():
            missing_cols = row.isna()
            # Replace NaN in numeric columns with the row mean
            data.loc[idx, missing_cols] = row_means[idx]  # Replace NaN with the row mean
        st.success("Missing values filled with row mean.")

    # Remove rows or columns with missing values
    st.subheader("Remove Missing Values")
    remove_option = st.radio(
        "Select an option to handle missing values:",
        ("None", "Remove rows with missing values", "Remove columns with missing values")
    )

    if remove_option == "Remove rows with missing values":
        data.dropna(axis=0, inplace=True)  # Drop rows with any missing values
        st.success("Rows with missing values have been removed.")
    
    elif remove_option == "Remove columns with missing values":
        data.dropna(axis=1, inplace=True)  # Drop columns with any missing values
        st.success("Columns with missing values have been removed.")

    # Remove unnecessary columns
    st.subheader("Remove Columns")
    columns_to_remove = st.multiselect("Select columns to remove:", options=data.columns)
    if columns_to_remove:
        data.drop(columns=columns_to_remove, inplace=True)

    # Select necessary rows
    st.subheader("Select Rows to Keep")
    rows_to_keep = st.multiselect("Select rows to keep (by index):", options=data.index.tolist())

    if st.button("Keep Selected Rows"):
        if rows_to_keep:
            data = data.loc[rows_to_keep]  # Keep only selected rows
            st.success(f"Rows {rows_to_keep} kept successfully!")
        else:
            st.warning("No rows selected.")
  
    # Reset the index to have rows numbered from 1 upwards
    data.reset_index(drop=True, inplace=True)  # Reset index and drop the old one
    data.index = data.index + 1  # Shift row numbers starting from 1
    
    # Fixing columns titles
    st.subheader("Rename Columns")
    if st.checkbox("Simplify column names (e.g., '2014 [YR2014]' → '2014')"):
        data.rename(columns=lambda x: x.split(" ")[0] if "YR" in x else x, inplace=True)

    # Display cleaned data
    st.subheader("Cleaned Dataset")
    st.write(data)

    # Download cleaned data
    st.subheader("Download Cleaned Dataset")
    st.download_button(label="Download CSV", data=data.to_csv(index=False), file_name="cleaned_dataset.csv", mime="text/csv")

'''
a problem in my previous code was not allowing me to calculate the mean values of the rest of the values
in order to replace the missing values. My mistake was that I was selecting the entire row including the name of the 
country, which is a string, and therefore was unable to a calculation.
Key Fix:
Filtering Numeric Columns: Before calculating row means, we use data.select_dtypes(include=['number']) to
select only the numeric columns for the mean calculation. This ensures that only numeric values are considered for
computing the row means and avoids issues with string columns. Now the code should work without the error, and it
 will fill missing values with the row mean for the numeric columns in the dataset.
'''
