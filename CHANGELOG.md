## v0.5.1 (2025-12-31)

### Fix

- improve docstring for ResultadoCalculo class

## v0.5.0 (2025-12-31)

### Feat

- add commitizen for versioning and changelogs
- implement adapters, entrypoints, and dependency injection
- migrate to domain-driven architecture and clean layers
- enhance method selection and calculation results display in app.py
- refactor soil type normalization with method mappings for improved clarity and maintainability
- enhance error messages for unsupported types and add cota_parada method in AokiVelloso, DecourtQaresma, and Teixeira classes
- implement calcular_capacidade_estaca function for pile capacity calculation
- add Streamlit app and CLI for Calculus-Core interface
- add Streamlit app and CLI for Calculus-Core interface
- add valid soil types selection and update SPT example data in Streamlit interface
- implement Streamlit interface for Calculus-Core package with SPT data input and capacity calculation
- add LICENSE file and update README with project details and usage examples
- add new Matos notebook for Teixeira calculations and SPT profile analysis
- implement Teixeira calculation methods and coefficient definitions
- add methods to calculate Np and admissible load capacity in AokiVelloso class
- add Schulze Tami notebook with Aoki Velloso and Decourt Quaresma calculations
- extend normalizar_tipo_solo function to include tabela parameter for improved soil type normalization
- enhance Aoki Velloso 1975 notebook with Laprovitera 1988 modifications and examples
- add AokiVelloso coefficients and factors for Laprovitera 1988 methodology
- update AokiVelloso and DecourtQuaresma notebooks to use correct function references
- refactor AokiVelloso class to integrate coefficient and factor definitions
- refactor DecourtQuaresma class to encapsulate calculation methods and coefficients
- add MetodoCalculo abstract class for foundation calculation methods
- implement calcular_capacidade_estaca function for pile load capacity calculation
- add example usage for calcular_aoki_velloso_1975 function with output display
- add Aoki and Velloso (1975) and Decourt Quaresma load capacity calculation notebooks
- implement Aoki and Velloso (1975) load capacity calculation for piles
- add confiavel parameter to PerfilSPT constructor for reliability tracking
- add normalization functions for soil and pile types, implement capacity calculation method
- implement Estaca and MedidaSPT classes with associated methods for calculations and data handling
- add calculations for lateral and point resistance
- implement Estaca class and Decourt-Quaresma calculation methods

### Fix

- correct test regex for cota validation message and add bump permissions
- update project version to 0.1.2 in pyproject.toml and uv.lock
- update project version to 0.1.1 in pyproject.toml
- update import statement for calcular_capacidade_estaca function
- update wheel package inclusion to include all source files
- update pygments and streamlit versions in uv.lock
- update import statements to relative paths in multiple files
- update soil type references in example usage for PerfilSPT
- correct k_kpa value for 'areia_silto_argilosa' and refactor obter_fatores_F1_F2 method
- enhance normalization for 'areia_com_pedregulhos' in normalizar_tipo_solo function
- add normalization for 'areia_com_pedregulhos' in Aoki Velloso method
- add Teixeira method support in calcular_capacidade_estaca function
- enhance soil type normalization for 'teixeira' method in normalizar_tipo_solo function
- update SPT measurement retrieval to include approximation in Teixeira class
- update kernel display name to .venv in multiple notebooks feat: add new Estude Engenharia notebook for Decourt Quaresma calculations
- update calcular_Nl method to use Estaca object and enforce NSPT limits
- correct intervalo_inicio calculation in calcular_Np method to use math.ceil
- adjust cota_parada calculation based on metodo_calculo type in calcular_capacidade_estaca function
- refactor DecourtQuaresma calculations and add method to compute admissible load capacity
- add type annotations for parameters in Estaca class and ensure cota_assentamento is an integer
- update 'comprimento' to 'cota_assentamento' in Aoki Velloso and Decourt Quaresma notebooks, adjust related calculations
- rename 'comprimento' to 'cota_assentamento' in Estaca model and update related calculations
- enable approximate measurement for cota below in DecourtQuaresma class
- improve depth validation in PerfilSPT class for approximate measurements
- update Estaca format to circular and adjust execution counts in Schulze Tami notebook
- correct variable name for settlement depth in AokiVelloso class
- correct variable name for settlement depth in DecourtQuaresma methods
- update cota_asentamento handling in calcular_decourt_quaresma function for accurate depth calculations
- add type hint for perfil_spt parameter in calcular_decourt_quaresma function
- correct spelling of 'hélice_contínua' and 'décourt_quaresma' in calculations
- update calcular_Np function to improve variable naming and error handling

### Refactor

- streamline calcular_Np and calcular_Nl functions, improve error handling and variable usage
