# py4madx library

Functions to help usage of cpymad for LHC analysis.

## pmadx
Functions for frequent actions in MADX for LHC analysis
*Note*: 
- The functions **twiss2df** and **table2df** converts MADX tables to dataframe. The default option is to use the raw elements name, i.e. without the ':' extension as index. If option 'comp' is used the complete MADX element name is used instead. 

## beambeam
Functions to install Beam Beam elements in LHC beams

The elements are defined with parameters as deferred assignments therefore can be updated according to needs. The information at all stages is contained in panda DataFrames. 

## qslice
Basic functions to slice a beam for HO Beambeam
