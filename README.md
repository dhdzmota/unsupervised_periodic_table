# unsupervised_periodic_table

This is a repo that contains all the information to represent a periodic table 
of elements with machine learning tools, mainly unsupervised learning. 

Project Organization
------------

    ├── README.md          <- The top-level README file for understanding this 
    │                         project.
    ├── data
    │   ├── raw            <- The original data dump.
    │   ├── interim        <- Data transformed but not as a final step.
    │   └── processed      <- Data used to train the final model. 
    │
    ├── models             <- Folder with the models and relevant information.
    │
    ├── notebooks          <- Contains jupyter notebooks or related files.
    │
    ├── references         <- Information relevant to the project context.
    │
    ├── results            <- Folder with the obtained results.
    │
    ├── src                <- Python code to run this project (main package).
    │   ├── data           <- Scripts for data read and transformations. 
    │   └── model          <- Scripts for ML workflow.
    │
    ├── general_pipeline.py  <- Steps to run and execute the main task of this
    │                           repo from data download to process and creation
    │                           of a model with corresponding results.
    │
    ├── setup.py           <- The requirements file for reproducing the
    │                         analysis environment.
    │
    └── requirements.txt   <- Makes project pip installable.
                              
Data
------------

The data of this analysis is obtained from the 
[PubChem webpage](https://pubchem.ncbi.nlm.nih.gov/periodic-table/), 
which is an official website of the United States government. In this cite,
one can find structured and machine-readable information on the Chemical Group Block, Atomic Mass, 
Standard State, Electronic Configuation, among other relevant fields 
(just to name a fiew). The next figure shows an example on the information that
the periodic table of this cite could contain.


![Periodic_Table_of_Elements_w_Names_PubChem.png](references%2FPeriodic_Table_of_Elements_w_Names_PubChem.png)

As relevant part of context, the periodic table as we know it today is managed by the 
[IUPAC](https://iupac.org), and this is relevant since PubChem is working with IUPAC to make this 
information available and downloadable. 

 In the `src/data/download_data.py` script, one can see how to obtain the `csv`
 file from this webpage. 

In this case, the main purpose of this analysis is to determine if machine 
learning techniques (mainly within an unsupervised scope) can reproduce some of
the patterns that are seen in the periodic table by considering the new 
available structured information that has been integrated to each element over 
the years. 

To do this a complete data science workflow was implemented, from de download 
and  cleaning of the data, to the feature engineering, additional process and 
further transformations of the information to finally develop some unsupervised 
models and as well some interpretability (with shap values). 

How to execute the code
------------
In this case, the execution to replicate the solution by implementing the 
following code is fairly simple (I recommend to make use of an empty virtual
environment when attempting to install the dependencies).

The first step, after cloning the repo, is to `pip install` the dependencies 
found in the `requirements.txt` file with:

`pip install -r requirements.txt`. 

Then it is as simple as executing the following command to download, process 
the information and generate an unsupervised model with the corresponding shap 
explicability:

`python general_pipeline.py`

This should be everything that must be done to execute the code. This will as 
well yield the results as images in the `results` folder and the relevant 
models and information will be saved in the `models` folder.


A fast glance to some results
------------
What one might find is that there are some elements that are somehow linked 
together. These elements are sub-groups and they are somehow intertwined 
with each other.

An example of this is the following image. 

![classification_09.png](results%2Fclassification_09.png)


In this case, we can see that the atomic numbers are: [3, 4, 11, 12, 20]. Which
correspond to Litium (Li), Beryllium(Be), Sodium (Na), Magnesium (Mg) and 
Calcium (Ca) respectively. In this specific instance Be, Mg and Ca belong to 
the same Element Group, and Li and Na belong to their own corresponding Group
too. These elements can be found together in the Periodic Table of Elements 
which can also tell us that they have relatively similar fields. 

The main reasons of similitud between these Elements can be found in the 
following figure which considers the shap values. 

![shap_classification_09.png](results%2Fshap_classification_9.0.png)

In this case, the most relevant features are (in order of importance):
1) Electron configuration highest orbital (is it s,p,d or f).
2) Electron configuration information count (after noble gas).
3) Electron configuration last orbital
4) Atomic radius over the atomic number (considering overlap).
5) Electron configuration electron hold. 


Additional Considerations
------------
This project is executed with `Python 3.8.10`. 

Generated by [`Daniel Hernández Mota`](https://www.dhdzmota.com).

Link to [github](https://www.github.com/dhdzmota)

References
------------
- National Center for Biotechnology Information (2023). 
Periodic Table of Elements. Retrieved November 6, 2023 
from https://pubchem.ncbi.nlm.nih.gov/periodic-table/.
- Vettigli, G. (2018) {MiniSom: minimalistic and NumPy-based
implementation of the Self Organizing Map. Retrieved November 6, 2023 from
https://github.com/JustGlowing/minisom/
- Lundberg, S. M. & Lee, S.-I. A unified approach to interpreting model
predictions. Adv. Neural Inf. Process. Syst. 30, 4768–4777 (2017).