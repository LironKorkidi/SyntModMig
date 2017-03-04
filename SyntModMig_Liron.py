"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import remi.gui as gui
from remi import start, App
import copy

class SyntModMig(App):
    def __init__(self, *args):
        super(SyntModMig, self).__init__(*args)
    
    def main(self):
        # Input & output tabs
        input_tab_container = self.input_tab_layout()
        output_tab_container = self.output_tab_layout()
        synt_mod_mig_tabs = gui.TabBox(width='80%')
        synt_mod_mig_tabs.add_tab (input_tab_container, 'Input Models', None)
        synt_mod_mig_tabs.add_tab (output_tab_container, 'Outputs', None)

        # Menu bar
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('File', width=100, height=30)
        m11 = gui.MenuItem('Save', width=100, height=30)
        m12 = gui.MenuItem('Open', width=100, height=30)
        m111 = gui.MenuItem('Save', width=100, height=30)
#        m111.set_on_click_listener(self.menu_save_clicked)
        m112 = gui.MenuItem('Save as', width=100, height=30)
#        m112.set_on_click_listener(self.menu_saveas_clicked)

        menu.append(m1)
        m1.append(m11)
        m1.append(m12)
        m11.append(m111)
        m11.append(m112)

        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        # Control buttons
        buttons_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        self.save = gui.Button('Save', width=100, height=30, margin='10px')
        self.save.set_on_click_listener(self.on_save)
        self.apply = gui.Button('Apply', width=100, height=30, margin='10px')
        self.apply.set_on_click_listener(self.on_apply)
        self.cancel = gui.Button('Cancel', width=100, height=30, margin='10px')
        self.cancel.set_on_click_listener(self.on_cancel)
        
        buttons_container.append (self.save)
        buttons_container.append (self.apply)
        buttons_container.append (self.cancel)
        
        synt_mod_mig = gui.Widget(width=1500, margin='0px auto') #the margin 0px auto centers the main container
        synt_mod_mig.style['display'] = 'block'
        synt_mod_mig.style['overflow'] = 'hidden'
        
        synt_mod_mig.append (menubar)
        synt_mod_mig.append (synt_mod_mig_tabs)
        synt_mod_mig.append (buttons_container)
        
        return synt_mod_mig
    
    def input_tab_layout(self):
        self.basic_symmetry = gui.DropDown.new_from_list(('ISO', 'VTI', 'ORT'), width=70, height=20)
        self.thickness = gui.SpinBox (500,  min=10,   max=10000, width=50, height=20, margin='10px')
        self.velocity  = gui.SpinBox (3000, min=1000, max=10000, width=50, height=20, margin='10px')
        self.delta1    = gui.SpinBox (0.07, min=-0.2, max=0.5, step=0.001, width=50, height=20, margin='10px')
        self.delta2    = gui.SpinBox (0.07, min=-0.2, max=0.5, step=0.001, width=50, height=20, margin='10px')
        self.epsilon1  = gui.SpinBox (0.1,  min=0,    max=0.5, step=0.001, width=50, height=20, margin='10px')
        self.epsilon2  = gui.SpinBox (0.1,  min=0,    max=0.5, step=0.001, width=50, height=20, margin='10px')
        self.azimuth   = gui.SpinBox (30,   min=0,    max=180,   width=50, height=20, margin='10px')
        
        self.basic_row = [(self.basic_symmetry, self.thickness, self.velocity, self.delta1, self.delta2, self.epsilon1, self.epsilon2, self.azimuth)]
        
        input_tab_container = gui.Widget(width=600, margin='0px auto') #the margin 0px auto centers the main container
        input_tab_container.style['display'] = 'block'
        input_tab_container.style['overflow'] = 'hidden'
                                   
        original_model_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        original_model_container.style['display'] = 'block'
        original_model_container.style['overflow'] = 'auto'
        self.original_model_lbl = gui.Label('Original Model Parameters', width=200, height=30, margin='10px')
        self.original_model_lbl.style['font-weight'] = 'bold'
        self.add_row      = gui.Button('Plus',  width=80, height=30, margin='10px')
        self.add_row.set_on_click_listener(self.on_add_row)        
        self.remove_row   = gui.Button('Minus', width=80, height=30, margin='10px')
        self.remove_row.set_on_click_listener(self.on_remove_row)
        self.reset_button = gui.Button('Reset', width=150, height=30, margin='10px')
        self.reset_button.set_on_click_listener (self.on_reset)
        original_model_container.append (self.original_model_lbl)
        original_model_container.append (self.add_row)
        original_model_container.append (self.remove_row)
        original_model_container.append (self.reset_button)
        
        self.original_model = gui.Table.new_from_list([('Symmetry', 'Thickness', 'Vp', 'Delta1', 'Delta2', 'Epsilon1','Epsilon2','Azimuth')], width=400, height=200, margin='10px')
        self.original_model.append_from_list(copy.copy(self.basic_row))
        self.original_model.append_from_list(copy.copy(self.basic_row))
        self.original_model.append_from_list(copy.copy(self.basic_row))
    
        preserve_mode_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        preserve_mode_container.style['display'] = 'block'
        preserve_mode_container.style['overflow'] = 'auto'
        self.preserve_mode_lbl = gui.Label('Preserved in background model', width=200, height=30, margin='10px')
        self.preserve_mode = gui.DropDown.new_from_list(('V. Time, Depth & Vnmo 0', 'V. Time & Depth 1', 'V. Time & Vnmo 2'), width=200, height=20)
        self.preserve_mode.set_value (0);
        preserve_mode_container.append (self.preserve_mode_lbl);
        preserve_mode_container.append (self.preserve_mode);
                                       
        background_model_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        background_model_container.style['display'] = 'block'
        background_model_container.style['overflow'] = 'auto'                                       
        self.background_model_lbl = gui.Label('Background Model Parameters', width=200, height=30, margin='10px')
        self.background_model_lbl.style['font-weight'] = 'bold'
        self.copy_params = gui.Button('Copy Parameters from Original Model', width=300, height=30, margin='10px')
        self.copy_params.set_on_click_listener(self.on_copy_parameters)
        background_model_container.append (self.background_model_lbl)
        background_model_container.append (self.copy_params)

        self.background_model = gui.Table.new_from_list([('Symmetry', 'Thickness', 'Vp', 'Delta1', 'Delta2', 'Epsilon1','Epsilon2','Azimuth')], width=400, height=200, margin='10px')
        self.background_model.append_from_list(copy.copy(self.basic_row))
        self.background_model.append_from_list(copy.copy(self.basic_row))
        self.background_model.append_from_list(copy.copy(self.basic_row))
    
        input_tab_container.append(original_model_container)
        input_tab_container.append(self.original_model)
        input_tab_container.append(preserve_mode_container)
        input_tab_container.append(background_model_container)
        input_tab_container.append(self.background_model)
        return input_tab_container
    
    def range_layout (self, title_str):
        range_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        range_container.style['display'] = 'block'
        range_container.style['overflow'] = 'auto'
        self.range_container_lbl  = gui.Label(title_str, width=100, height=30, margin='0px')
        self.range_lbl = gui.Label('-', width=20, height=30, margin='1px')
        self.step_lbl  = gui.Label('Step', width=50, height=30, margin='1px')
        self.range_container_first = gui.SpinBox (1,   min=1, max=1000, width=50, height=30, margin='0px')
        self.range_container_last = gui.SpinBox  (100, min=1, max=1000, width=50, height=30, margin='0px')
        self.range_container_step = gui.SpinBox  (1,   min=1, max=100,  width=50, height=30, margin='0px')
        range_container.append (self.range_container_lbl)
        range_container.append (self.range_container_first)
        range_container.append (self.range_lbl) 
        range_container.append (self.range_container_last)
        range_container.append (self.step_lbl)
        range_container.append (self.range_container_step)
        return range_container
    
    def output_range_layout (self):
        inline_range_container = self.range_layout ('Inline')
        xline_range_container  = self.range_layout ('Crossline')
        
        range_container = gui.Widget(width='100%', margin='0px')
        range_container.style['display'] = 'block'
        range_container.style['overflow'] = 'auto'
        self.output_range_lbl  = gui.Label('Output Range', width=200, height=30, margin='0px')
        range_container.append (self.output_range_lbl)
        range_container.append (inline_range_container)
        range_container.append (xline_range_container)
        return range_container
        
    def output_modeling_layout (self):
        output_modeling_container = gui.Widget()
        output_modeling_container.style['display'] = 'block'
        output_modeling_container.style['overflow'] = 'auto'
        
        modeling_range_container = self.output_range_layout()
        
        self.modeling_sr_geom_lbl  = gui.Label('Source-Receiver Geometry: Spiral OVT', width=400, height=50, margin='0px')

        modeling_sr_geom_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        modeling_sr_geom_container.style['display'] = 'block'
        modeling_sr_geom_container.style['overflow'] = 'auto'

        self.modeling_sr_max_offset_lbl = gui.Label ('Max. Offset', width=100, height=30, margin='0px')
        self.modeling_sr_max_offset = gui.SpinBox (5000, min=100, max=10000, width=50, height=30, margin='0px')
        self.modeling_sr_nodes_num_lbl  = gui.Label ('Nodes', width=50, height=30, margin='0px')
        self.modeling_sr_nodes_num = gui.SpinBox (500, min=100, max=10000, width=50, height=30, margin='0px')
        
        modeling_sr_geom_container.append (self.modeling_sr_max_offset_lbl)
        modeling_sr_geom_container.append (self.modeling_sr_max_offset)
        modeling_sr_geom_container.append (self.modeling_sr_nodes_num_lbl)
        modeling_sr_geom_container.append (self.modeling_sr_nodes_num)

        modeling_output_maps_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        modeling_output_maps_container.style['display'] = 'block'
        modeling_output_maps_container.style['overflow'] = 'auto'            
        self.modeling_maps_original_model_lbl = gui.CheckBoxLabel('Output Volumes and Maps of Original Model', True, width=300, height=30, margin='0px')
        modeling_output_maps_container.append (self.modeling_maps_original_model_lbl)
        
        modeling_domain_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        modeling_domain_container.style['display'] = 'block'
        modeling_domain_container.style['overflow'] = 'auto'         
        self.domain_lbl  = gui.Label('Domain:', width=100, height=30, margin='0px')
        self.modeling_domain_depth = gui.CheckBoxLabel('Depth', True, width=100, height=30, margin='0px')
        self.modeling_domain_tm = gui.CheckBoxLabel('Time Migrated', False, width=200, height=30, margin='0px')
        modeling_domain_container.append (self.domain_lbl)
        modeling_domain_container.append (self.modeling_domain_depth)
        modeling_domain_container.append (self.modeling_domain_tm)
        
        self.modeling_output_lbl  = gui.CheckBoxLabel('Modeling Output', width=200, height=30, margin='10px')
        self.modeling_output_lbl.style['font-weight'] = 'bold'
        output_modeling_container.append (self.modeling_output_lbl)
        output_modeling_container.append (modeling_range_container)
        output_modeling_container.append (self.modeling_sr_geom_lbl)
        output_modeling_container.append (modeling_sr_geom_container)
        output_modeling_container.append (modeling_output_maps_container)
        output_modeling_container.append (modeling_domain_container)
        
        return output_modeling_container
        
    def output_migation_layout (self):
        output_migration_container = gui.Widget()
        output_migration_container.style['display'] = 'block'
        output_migration_container.style['overflow'] = 'auto'
        
        migration_range_container = self.output_range_layout()

        self.output_domain_of_migrated_lbl  = gui.Label('Output Domain of Migrated Gathers: ES360', width=300, height=50, margin='0px')        
        migration_output_domain = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        migration_output_domain.style['display'] = 'block'
        migration_output_domain.style['overflow'] = 'auto'

        self.migration_output_max_angle_lbl = gui.Label ('Max. Angle', width=100, height=30, margin='0px')
        self.migration_output_max_angle = gui.SpinBox (30, min=10, max=90, width=50, height=30, margin='0px')
        self.migration_output_nodes_num_lbl  = gui.Label ('Nodes', width=50, height=30, margin='0px')
        self.migration_output_nodes_num = gui.SpinBox (500, min=100, max=10000, width=50, height=30, margin='0px')
        
        migration_output_domain.append (self.migration_output_max_angle_lbl)
        migration_output_domain.append (self.migration_output_max_angle)
        migration_output_domain.append (self.migration_output_nodes_num_lbl)
        migration_output_domain.append (self.migration_output_nodes_num)
        
        migration_output_maps_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        migration_output_maps_container.style['display'] = 'block'
        migration_output_maps_container.style['overflow'] = 'auto'            
        self.migration_maps_original_model_lbl = gui.CheckBoxLabel('Output Volumes and Maps of Original Model', True, width=300, height=30, margin='10px')
        migration_output_maps_container.append (self.migration_maps_original_model_lbl)
        
        migration_domain_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        migration_domain_container.style['display'] = 'block'
        migration_domain_container.style['overflow'] = 'auto'         
        self.migration_domain_depth = gui.CheckBoxLabel('Depth', True, width=100, height=30, margin='0px')
        self.migration_domain_tm = gui.CheckBoxLabel('Time Migrated', False, width=200, height=30, margin='0px')
        migration_domain_container.append (self.domain_lbl)
        migration_domain_container.append (self.migration_domain_depth)
        migration_domain_container.append (self.migration_domain_tm)
        
                
        self.migration_output_lbl  = gui.CheckBoxLabel('  Migration Output', width=200, height=30, margin='0px')
        self.migration_output_lbl.style['font-weight'] = 'bold'
        output_migration_container.append (self.migration_output_lbl)
        output_migration_container.append (migration_range_container)
        output_migration_container.append (self.output_domain_of_migrated_lbl)
        output_migration_container.append (migration_output_domain)
        output_migration_container.append (migration_output_maps_container)
        output_migration_container.append (migration_domain_container)
        
        return output_migration_container

    def output_tab_layout (self):
        output_tab_container = gui.Widget(margin='0px auto') #the margin 0px auto centers the main container
        output_tab_container.style['display'] = 'block'
        output_tab_container.style['overflow'] = 'auto'

        output_model_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        output_model_container.style['display'] = 'block'
        output_model_container.style['overflow'] = 'auto'
        
        output_modeling_container = self.output_modeling_layout ()
        output_migration_container = self.output_migation_layout ()
        output_model_container.append (output_modeling_container)
        output_model_container.append (output_migration_container)
        
        output_files_container = gui.Widget()
        output_files_container.style['display'] = 'block'
        output_files_container.style['overflow'] = 'auto'
        
        output_name_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        output_name_container.style['display'] = 'block'
        output_name_container.style['overflow'] = 'auto'
        self.output_files_name_lbl  = gui.Label('Name', width=200, height=30, margin='10px')
        self.output_files_name = gui.TextInput (width=200, height=30, margin='10px')
        self.output_files_name.set_value ('Synthetic Data')
        output_name_container.append (self.output_files_name_lbl)
        output_name_container.append (self.output_files_name)
        
        output_class_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        output_class_container.style['display'] = 'block'
        output_class_container.style['overflow'] = 'auto'
        self.output_files_class_lbl  = gui.Label('Class', width=200, height=30, margin='10px')
        self.output_files_class = gui.TextInput (width=200, height=30, margin='10px')
        self.output_files_class.set_value ('SyntModMig')
        output_class_container.append (self.output_files_class_lbl)
        output_class_container.append (self.output_files_class)

        output_comment_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        output_comment_container.style['display'] = 'block'
        output_comment_container.style['overflow'] = 'auto'
        self.output_files_comment_lbl  = gui.Label('Comment', width=200, height=30, margin='10px')
        self.output_files_comment = gui.TextInput (width=200, height=30, margin='10px')
        self.output_files_comment.set_value ('-')
        output_comment_container.append (self.output_files_comment_lbl)
        output_comment_container.append (self.output_files_comment)
        
        output_data_container = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        output_data_container.style['display'] = 'block'
        output_data_container.style['overflow'] = 'auto'
        self.output_files_class_lbl  = gui.Label('Data Format', width=200, height=30, margin='10px')
        self.ddropdown = gui.DropDown.new_from_list(('SEG-Y', 'SEG-X'), width=200, height=30)
        output_data_container.append (self.output_files_class_lbl)
        output_data_container.append (self.ddropdown)
        
        self.output_files_lbl = gui.Label('Output Files', width=200, height=30, margin='10px')
        self.output_files_lbl.style['font-weight'] = 'bold'
        output_files_container.append (self.output_files_lbl)
        output_files_container.append (output_name_container)
        output_files_container.append (output_class_container)
        output_files_container.append (output_comment_container)
        output_files_container.append (output_data_container)
        
        output_tab_container.append (output_model_container)
        output_tab_container.append (output_files_container)
        
        return  output_tab_container
    
    def on_add_row (self, widget):
        self.original_model.append_from_list (copy.copy(self.basic_row))
        self.background_model.append_from_list (copy.copy(self.basic_row))
        print self.original_model.children.keys()
        print self.background_model.children.keys()

    def on_remove_row (self, widget):
        number_of_rows = len (self.original_model.children.keys())
        if number_of_rows > 1:
            self.original_model.remove_child (self.original_model.children[self.original_model.children.keys () [1]])
            self.background_model.remove_child (self.background_model.children[self.background_model.children.keys () [1]])
        print self.original_model.children.keys()
        print self.background_model.children.keys()
        
    def on_reset (self, widget):
        self.original_model.empty (True)
        self.original_model.append_from_list (copy.copy(self.basic_row))
        self.original_model.append_from_list (copy.copy(self.basic_row))
        self.original_model.append_from_list (copy.copy(self.basic_row))
        self.background_model.empty(True)
        self.background_model.append_from_list (copy.copy(self.basic_row))
        self.background_model.append_from_list (copy.copy(self.basic_row))
        self.background_model.append_from_list (copy.copy(self.basic_row))

    def on_copy_parameters (self, widget):
        self.background_model.empty (True)
        for cur_key in self.original_model.children.keys():
            if (cur_key != 'title'):
                self.background_model.append (copy.copy(self.original_model.children[cur_key]), cur_key)

    def on_save (self, widget):
        print "Save parameters"
        
    def on_apply (self, widget):
        print "Do the actual work!"
        
    def on_cancel (self, widget):
        self.on_reset (self, widget)
        
if __name__ == "__main__":
    start(SyntModMig, title="Synthetic Modeling", standalone=False)

