name: "System update 002",
summary: Module to allocate system update 2

important files within this module
==================================
Grant Wizard form
<form string="Grant Report">
                    <group>
                        <group>
                            <field name="start_date" required="1"/>
                        </group>
                        <group>
                            <field name="end_date" required="1"/>
                        </group>
                    </group>
                    <group>
                        <field name="type" invisible="1"/>
                        <field name="all_branch"
                           attrs="{'invisible': [('type', 'in', ['status_branch', 'status_branch_cons'])]}"/>
                        <field name="branch_id" options="{'no_open': True, 'no_create': True}"
                           attrs="{'required': [('all_branch', '=', False)], 'invisible': [('type', 'in', ['status_branch', 'status_branch_cons'])]}"/>
                        <field name="status" invisible="0"/>
                    	<field name="report_type" invisible="1"/>
                    	<field name="grant_threshold" invisible="0"/>
                    </group>
                
                    <footer>
                        <button name="get_grant_report" string="Print" type="object" class="oe_highlight"/>
                        or
                        <button string="Cancel" class="oe_highlight" special="cancel"/>
                    </footer>
                </form>

Report
                                    <div>

                                        <p align="center">
                                            <h3>Grant Report
                                            </h3>
                                        </p>
                                        <br/>
                                    </div>
                                    <div>
                                        <div class="col-xs-4 text-left">
                                            <h4>
                                                <b>START DATE :
                                                    <u>
                                                        <t t-esc="dates.get('s_date')"/>
                                                    </u>
                                                </b>
                                            </h4>
                                        </div>
                                        <div class="col-xs-4 text-right">
                                            <h4>
                                                <b>END DATE :
                                                    <u>
                                                        <t t-esc="dates.get('e_date')"/>
                                                    </u>
                                                </b>
                                            </h4>
                                        </div>
                    					<div class="col-xs-4 text-right">
                                            <h4>
                                                <b>Status :
                                                    <u>
                                                        <t t-esc="dates.get('type')"/>
                                                    </u>
                                                </b>
                                            </h4>
                                        </div>
                                        <br/>
                                        <div class="col-xs-4 text-right">
                                            <h4>
                                                <b>Branch :
                                                    <u>
                                                        <t t-esc="dates.get('branch')"/>
                                                    </u>
                                                </b>
                                            </h4>
                                        </div>
                                        <div class="col-xs-4 text-right">
                                            <h4>
                                                <b>Threshold :
                                                    <u>
                                                        <t t-esc="dates.get('threshold')"/>
                                                    </u>
                                                </b>
                                            </h4>
                                        </div>
                    
                                    </div>






grant application form view 
						
						
                      <br/>
                      <div class="oe_button_box" style="align:right;text-align:right">
                        <button class="btn btn-sm oe_stat_button" style="width:220px !important;font-weight:bold;font-size:" name="calculated_grants" string="" type="object">
                               <div class="fa fa-fw o_button_icon fa-ticket"></div>
                               <field name="x_grant_applications_count" readonly="1" widget="statinfo" style="padding-left:1px;"/>
                               
                               
                        </button>
                      </div>
                      <br/>

voucher application form view

                        
                        <div class="col-md-12" style="align:right;text-align:right">
                              <button name="calculated_vouchers" style="font-size:12px;font-weight:bold;align:right;text-align:right;" type="object" >
                              <label for="x_total_approved_vouchers" string="No of Vouchers received"/>
                            
                            <!---->
                            <h5>
                                <field name="x_total_approved_vouchers" readonly="1"/>
                            </h5>
                            </button>
                            </div>
                            
                      upgraded 
                      <br/>
                      <div class="oe_button_box" style="align:right;text-align:right">
                        <button class="btn btn-sm oe_stat_button" style="width:220px !important;font-weight:bold;font-size:" name="calculated_vouchers" string="" type="object">
                               <div class="fa fa-fw o_button_icon fa-ticket"></div>
                               <field name="x_total_approved_vouchers" readonly="1" widget="statinfo" style="padding-left:1px;"/>
                               
                               
                        </button>
                      </div>
                      <br/>
                      
                            
                            /////
                       <div class="col-md-12">
                          <h4>
                            <field name="x_flag"/>
                          </h4>
                       </div>
JS changes


//if (currentTab == 1 && !validate2ndPage()) return false;
	//line above replaced by the below:
	if ($("#regForm").attr("action").indexOf("voucher") != -1 && currentTab == 1){
		if (xl.length < 1){
			alert("Please select atleast one Business support services");
			return;
		} else if (xl.length >= 5){
			alert("You can only qualify to a maximum of 4 vouchers in a life time");
			return;
					
  		}
			
	}
	//if (currentTab == 3 && !validate4thPage()) return false;
	//reduce execution speed for the above to work
                            
                            
                        