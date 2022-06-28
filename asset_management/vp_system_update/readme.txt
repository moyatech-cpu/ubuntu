1. Add the following on the vp19 report
<table style="padding-left: 0px;padding-right: 0px;border-style: solid;border-width: 1px;width:100%">
	                        		
	                        		<tr>
                            				<th style="border: 1px solid black;padding: 5px;">
                            					Name
                            				</th>
                            				<th style="border: 1px solid black;padding: 5px;">
                            					Phone
                            				</th>
                            				<th style="border: 1px solid black;padding: 5px;">
                            					Email
                            				</th>
                            				<th style="border: 1px solid black;padding: 5px;">
                            					Payment Status
                            				</th>
                            				
                            		</tr>	
                            		<t t-foreach="data['service_providers']" t-as="v_data">
                            		<tr>
                            				<td style="border: 1px solid black;padding: 5px;">
                            					<t t-esc="v_data['display_name']"/>
                            				</td>
                            				<td style="border: 1px solid black;padding: 5px;">
                            					<t t-esc="v_data['phone']"/>
                            				</td>
                            				<td style="border: 1px solid black;padding: 5px;">
                            					<t t-esc="v_data['email']"/>
                            				</td>
                            				<td style="border: 1px solid black;padding: 5px;">
                            					<t t-esc="v_data['payment_status']"/>
                            				</td>
                            			</tr>
                            		</t>
                            		
                            	</table>
                            	

2. BCS Existing form should have the following
<group colspan="4">
                            <!-- <group>
                            	<field name="date" readonly="1"/>
                            	<field name="num_of_applications"/> 
                            	<field name="branch"/>
                            </group>-->
                            <field name="service_provider" attrs="{'readonly': [('status', '!=', 'new')]}"/>
                            <br/>
                            <group colspan="4">
                            	<div class="col-md-12" style="padding-left: 0px;padding-right: 0px;border-style: solid;border-width: 0px;">
                            	<notebook>
                    