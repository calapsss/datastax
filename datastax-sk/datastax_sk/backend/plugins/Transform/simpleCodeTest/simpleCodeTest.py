
def test_code(code, filename):
    import streamlit as st
    import pandas as pd

    #access temp folder to retreive file
    df = pd.read_csv('../../../temp/' + filename)

    try:
        print("Executing Code...")
        exec(code)
        print("Success!")
        return "success"
    except Exception as e:
        print("Error: ", e)
        return(e)

