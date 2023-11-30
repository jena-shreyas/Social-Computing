This assignment explores the use of various approaches for the following requirements :

## Tasks
  - Intent Recognition
  - Entity Extraction

## Dataset
  - Multilingual medical query dataset (sourced from platforms like [WebMD](https://webmd.com) and [1mg](https://www.1mg.com/))
  - Link : [here](https://github.com/indichealth/indic-health-demo)
 
## Steps
  - **Intent Recognition**

    - Classify medical queries into four types - `Drug`, `Disease`, `Treatment` or `Other`.
    - *English*
      
      - Use the following models (notebook links provided):
        - [SVM](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/IR/ir_svm_en.ipynb)
        - [RoBERTa](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/IR/ir_rob_en.ipynb)
        - [BioClinicalBERT](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/IR/ir_bcbert_en.ipynb)
          
    - *Hindi*
      
      - Use the following models :
        - [XLMR](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/IR/ir_xlmr_hi.ipynb)
        - [Back-translation to English and then BioClinicalBERT](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/IR/ir_dtrans_hi.ipynb)
        - [Bridge-language back translation and then BioClinicalBERT `(Bengali -> Hindi (bridge) -> English)`](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/IR/ir_bridge_hi.ipynb)

  - **Entity Extraction**

    - Annotate medical queries using BIO tags based on annotated entities
    - Perform Entity Extraction on medical queries using the given BIO tags
    - *English*
      
      - Use the following models :
        - [SVM](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/EE/ee_svm_hi.ipynb)
        - [RoBERTa](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/EE/ee_rob_en.ipynb)
        - [BioClinicalBERT](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/EE/ee_bcbert_en.ipynb)
          
    - *Hindi*
      
      - Use the following models :
        - [XLMR](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/EE/ee_xlmr_hi.ipynb)
        - [Back-translation to English and then BioClinicalBERT](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/EE/ee_dtrans_hi.ipynb)
        - [Bridge-language back translation and then BioClinicalBERT `(Bengali -> Hindi (bridge) -> English)`](https://github.com/jena-shreyas/Social-Computing/blob/master/Assn2/20CS30049_ShreyasJena_Assignment2/notebooks/EE/ee_bridge_hi.ipynb)
    
