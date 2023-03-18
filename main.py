import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio


st.title('Predict Your Protein here! 🍖🧬')
st.write('Here we are using [*ESMFold*](https://esmatlas.com/about) to predict your single sequence protein structure using the ESM-2 language model. You can learn more about the model, just click [HERE](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and you can check their news article publsihed on [Nature](https://www.nature.com/articles/d41586-022-03539-1).')


def load_protein(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'stick':{'color':'spectrum'}})
    pdbview.setBackgroundColor('#0E1117')
    pdbview.zoomTo()
    pdbview.zoom(1, 750)
    pdbview.spin(False)
    showmol(pdbview, height = 500,width=800)
    
def cartoon_protein(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{'color':'spectrum'}})
    pdbview.setBackgroundColor('#0E1117')
    pdbview.zoomTo()
    pdbview.zoom(1, 750)
    pdbview.spin(True)
    showmol(pdbview, height = 500,width=800)


my_seq= "QCTGGADCTSCTGACTGCGNCPNAVTCTNSQHCVKANTCTGSTDCNTAQTCTNSKDCFEANTCTDSTNCYKATACTNSSGCPGH"
txt = st.text_area('Enter your sequence', my_seq, height=275)


def update(seq=txt):

    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers={'Content-Type': 'application/x-www-form-urlencoded',}, data=seq)
    name = seq[:3] + seq[-3:]
    pdb_file = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_file)

    structure = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(structure.b_factor.mean(), 4)

    
    st.subheader('Here is your protein!')
    load_protein(pdb_file)
    cartoon_protein(pdb_file)
    
    st.subheader('How confident are we with this prediction?')
    st.write('Well on a scale from 0-100.')
    st.info(f'The level of accuracy is: {b_value*100}%')

    st.download_button(
        label = "Download your protein's PDB",
        data = pdb_file,
        file_name='predicted_protein.pdb',
        mime='text/plain',
    )

predict = st.button('Predict', on_click=update)
