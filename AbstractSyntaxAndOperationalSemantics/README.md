# Abstract Syntax and Operational semantics in metaDepth

### Goal
Our goal was to design a meta-model for our domain-specific
(modelling) language (DSL), specify operational semantics for the language, create instances of this meta-model and verify conformance between (instance) model and meta-model. While using the textual modelling tool [MetaDepth](http://metadepth.org) and its action&constraint language EOL.

### Outcome
A visual representation of our Abstract Syntax can be seen below.
![A visual representation of our Abstract Syntax](/AbstractSyntaxAndOperationalSemantics/AbstractSyntax.png)


### Files
- [AbstractSyntax](/AbstractSyntaxAndOperationalSemantics/AbstractSyntax.png): A visual representation of the Abstract Syntax
- [README.md](/AbstractSyntaxAndOperationalSemantics/README.md): This file.
- [run.sh](/AbstractSyntaxAndOperationalSemantics/run.sh): Script file to start the MetaDepth tool.
- [Models/](/AbstractSyntaxAndOperationalSemantics/Models): A collection of valid and invalid models that have been used for testing
- [WaterwayModeligInMetaDepth.pdf](/AbstractSyntaxAndOperationalSemantics/WaterwayModeligInMetaDepth.pdf): The project requirements.
- [WMS.eol](/AbstractSyntaxAndOperationalSemantics/WMS.eol): The operational semantics of the Water Modeling System.
- [WMS.mdc](/AbstractSyntaxAndOperationalSemantics/WMS.mdc): MedaDepth helper file.
- [WMS.mdepth](/AbstractSyntaxAndOperationalSemantics/WMS.mdepth): The abstract syntax of the Water Modeling System.
- [WMS.txt](/AbstractSyntaxAndOperationalSemantics/WMS.txt): Generated graph representation of the Abstract syntax + a onotological instance.