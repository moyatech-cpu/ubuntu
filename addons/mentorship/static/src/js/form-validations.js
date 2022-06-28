odoo.define('mentorship.form_validations', function(require) {
    $(document).ready(function () {
        var counter = 0;
        if($('#experience_table')){
            $("#addrow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><input type="text" class="form-control" name="course"/></td>';
                cols += '<td><input type="text" class="form-control" name="institutionOrganisation"/></td>';
                cols += '<td><input type="number" class="form-control" name="duration"/></td>';
                cols += '<td><input type="date" name="when" class="form-control"/></td>'

                cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#experience_table.order-list").append(newRow);
                counter++;
            });
        }

        if($('#motivation_table')){
            $("#addmotivationrow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><textarea class="form-control motivation" name="motivationText"/></td>';

                cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#motivation_table.order-list").append(newRow);
                counter++;
            });
        }

        if($('#supporting_doc_table')){
            $("#adddocrow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><input type="file" class="form-control" required="required" name="supportingdoc'+ counter + '"/></td>';

                cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#supporting_doc_table.order-list").append(newRow);
                counter++;
            });
        }

        $("table.order-list").on("click", ".ibtnDel", function (event) {
            $(this).closest("tr").remove();
            counter -= 1
        });

        $('input[name="legalEntity"]').on('change', function(e){
            if($(this).val() == 'other'){
                if($(this).is(':checked')){
                    $('input[name="legalEntityChar"]').removeClass('hidden');
                }
                else{
                    $('input[name="legalEntityChar"]').addClass('hidden');
                }
            }
        });

        $('input[name="slegalEntity"]').on('change', function(e){
            if($(this).val() == 'other'){
                if($(this).is(':checked')){
                    $('input[name="slegalEntityChar"]').removeClass('hidden');
                }
                else{
                    $('input[name="slegalEntityChar"]').addClass('hidden');
                }
            }
        });

        if($('mentorship-application')){
            $('#mentorship-application').on('submit', function(event) {
                event.preventDefault();
                var values = {};
                $.each($(this).serializeArray(), function(i, field) {
                    values[field.name] = field.value;
                });
                if (values['application_type'] == "mentee_application"){
                    var areas = [];
                    var support = [];
                    var skillsTraining_ids = [];
                    var motivation_ids = [];
                    var slegalEntity = [];
                    var legalEntity = [];
                    var sector = [];
                    $.each($("input[name='areasSupport']:checked"), function(){
                        areas.push(parseInt($(this).val()));
                    });
                    $.each($("input[name='areasSupport']:checked"), function(){
                        areas.push(parseInt($(this).val()));
                    });
                    $.each($("input[name='slegalEntity']:checked"), function(){
                        if($(this).val() != 'other'){
                            slegalEntity.push(parseInt($(this).val()));
                        }
                    });
                    $.each($("input[name='legalEntity']:checked"), function(){
                        if($(this).val() != 'other'){
                            legalEntity.push(parseInt($(this).val()));
                        }
                    });
                    $.each($("input[name='sector']:checked"), function(){
                        sector.push(parseInt($(this).val()));
                    });
                    $('#experience_table tbody tr').each(function(){
                        var r_val = {}
                        r_val['course'] = $(this).find('td input[name="course"]').val();
                        r_val['institutionOrganisation'] = $(this).find('td input[name="institutionOrganisation"]').val();
                        r_val['duration'] = $(this).find('td input[name="duration"]').val();
                        r_val['when'] = $(this).find('td input[name="when"]').val();
                        skillsTraining_ids.push(r_val);
                    });
                    $('#motivation_table tbody tr').each(function(){
                        var r_val = {}
                        r_val['motivationText'] = $(this).find('td .motivation').val();
                        motivation_ids.push(r_val);
                    });
                    values['areasSupport'] = areas;
                    values['mentoringSupport'] = support;
                    values['skillsTraining_ids'] = skillsTraining_ids;
                    values['motivation_ids'] = motivation_ids;
                    values['slegalEntity'] = slegalEntity;
                    values['legalEntity'] = legalEntity;
                    values['sector'] = sector;
                }
                if (values['application_type'] == "mentor_application"){
                    var sector = [];
                    var business_type = [];
                    $.each($("input[name='sector']:checked"), function(){
                        sector.push(parseInt($(this).val()));
                    });
                    $.each($("input[name='business_type']:checked"), function(){
                        business_type.push(parseInt($(this).val()));
                    });
                    values['sector'] = sector;
                    values['business_type'] = business_type;
                }
                $('input[name="formatted_data"]').val(JSON.stringify(values));
                event.currentTarget.submit();

            });
        }
    });
});