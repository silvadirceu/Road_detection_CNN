from abstractions.component import Component
from components.display import DisplayComponent
from components.styles import StylesComponent
from components.report_features_checkbox import ReportFeatureCheckboxComponent
from components.table import TableComponent
from components.upload_file import UploadFileComponent

__report_features_component: Component = ReportFeatureCheckboxComponent()
__upload_file_component: Component = UploadFileComponent()
__styles_component: Component = StylesComponent()
__table_component: Component = TableComponent()
__display_component: Component = DisplayComponent()

report_features = __report_features_component.render
upload_file = __upload_file_component.render
table = __table_component.render
styles = __styles_component.render
display = __display_component.render