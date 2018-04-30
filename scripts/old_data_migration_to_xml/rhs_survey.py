#	Script written on Python 3.6
# 	Author : Parag Fulzele
#	Description : Methods to convert RHS survey into xml
#

import uuid
import traceback
import copy

from common import *

# dictionary use to set and export data into xml
#Form number 102
gl_rhs_xml_dict = {
	"__version__": "vbqmmSmBxRL4Yi6CnZKEMw",
	"_submission_time": None,
    "_status": None,
    "_submitted_by": None,
    "_xform_id_string":"a2NE2CCR6izXK22H2Aa9Kr",
    "start":None,
    "end":None,
    "admin_ward": None,
    "slum_name": None,
    "Date_of_survey":None,
    "Name_s_of_the_surveyor_s": None,
    "Household_number": None,
    "Type_of_structure_occupancy": None,
    "Type_of_unoccupied_house": None,
    "Parent_household_number": None,
    "group_og5bx85": {
      "Full_name_of_the_head_of_the_household":None,
      "Type_of_survey": None
    },
    "group_el9cl08": {
      "Enter_the_10_digit_mobile_number": None,
      "Aadhar_number": None,
      "Number_of_household_members": None,
      "Do_you_have_any_girl_child_chi": None,
      "How_many": None,
      "Type_of_structure_of_the_house": None,
      "Ownership_status_of_the_house": None,
      "House_area_in_sq_ft": None,
      "Type_of_water_connection": None,
      "Facility_of_solid_waste_collection": None,
      "Does_any_household_m_n_skills_given_below": None
    },
  "group_oi8ts04": {
      "Have_you_applied_for_individua": None,
      "Type_of_SBM_toilets": None,
      "How_many_installments_have_you": None,
      "When_did_you_receive_ur_first_installment": None,
      "When_did_you_receive_r_second_installment": None,
      "When_did_you_receive_ur_third_installment": None,
      "If_built_by_contract_ow_satisfied_are_you": None,
      "Status_of_toilet_under_SBM": None,
      "What_was_the_cost_in_to_build_the_toilet": None,
      "C1": None,
      "C2": None,
      "C3": None,
      "C4": None,
      "C5": None,
      "Current_place_of_defecation": None,
      "Is_there_availabilit_onnect_to_the_toilet": None,
      "Are_you_interested_in_an_indiv": None,
      "What_kind_of_toilet_would_you_like": None,
      "Under_what_scheme_wo_r_toilet_to_be_built": None,
      "If_yes_why": None,
      "If_no_why": None,
      "What_is_the_toilet_connected_to": None,
      "Who_all_use_toilets_in_the_hou": None,
      "Reason_for_not_using_toilet": None,
      "OD1": None
    },
    "Enter_household_number_again": None,
	"meta": {
		"instanceID": None
	},
	"formhub": {
		"uuid": "c323c30949394726ae99e5116cebde54"
	}
}


# gl_rhs_xml_dict = {
#	'formhub' : {
#		'uuid' : None
#	},
#	'start' : None,
#	'end' : None,
#	'group_ce0hf58' : {
#		'city' : None,
#		'admin_ward' : None,
#		'slum_name' : None,
#		'date_of_rhs' : None,
#		'name_of_surveyor_who_collected_rhs_data' : None,
#		'house_no' : None,
#		'Type_of_structure_occupancy' : None
#	},
#	'group_ye18c77' : {
#		'group_ud4em45' : {
#			'what_is_the_full_name_of_the_family_head_' : None,
#			'mobile_number' : None,
##			'adhar_card_number' : None
#		},
#		'group_yw8pj39' : {
#			'what_is_the_structure_of_the_house' : None,
#			'what_is_the_ownership_status_of_the_house' : None,
#			'number_of_family_members' : None,
#			'Do_you_have_a_girl_child_under' : None,
#			'if_yes_how_many_' : None,
#			'house_area_in_sq_ft' : None,
#			'Current_place_of_defecation_toilet' : None,
#			'does_any_member_of_your_family_go_for_open_defecation_' : None,
#			'where_the_individual_toilet_is_connected_to_' : None,
#			'type_of_water_connection' : None,
#			'facility_of_waste_collection' : None,
#			'Are_you_interested_in_individu' : None,
#			'if_yes_why_' : None,
#			'if_no_why_' : None,
#			'type_of_toilet_preference' : None,
#			'Have_you_applied_for_indiviual' : None,
#			'How_many_installements_have_yo' : None,
#			'when_did_you_receive_the_first_installment_date' : None,
#			'when_did_you_receive_the_second_installment_date' : None,
#			'what_is_the_status_of_toilet_under_sbm_' : None,
#			'Does_any_family_members_has_co' : None
#		},
#	},
#	'__version__' : None,
#	'meta' : {
#		'instanceID' : None
#	}
#}
# This string is ised for debugging for running the script for selected slum and selected house hold. 

######
#####To be made empty when running for production
######
#run_script_for_selected_slum_household = " and household.slum_id = 556 "
#run_script_for_selected_slum_household = " and household.slum_id = 615 and household.household_code = '0011' "
run_script_for_selected_slum_household = ""
## RHS survey queries
# get list of all household in all slums for survey
qry_rhs_slum_household_survey_list = "select distinct household.slum_id, household.household_code from survey_fact f \
join slum_data_household household on household.id = f.object_id \
join survey_survey s on s.id = f.survey_id join survey_project p on p.id = s.project_id \
where s.id = %s and p.id = %s and f.content_type_id = 27 " + run_script_for_selected_slum_household + " \
order by household.slum_id, household.household_code asc"

# get list of all question and answer for all household in slum
qry_rhs_survey_slum_household_question_answer = "(select household1.household_code, '-1' as question_id, to_char(min(f1.updated_on),'YYYY-MM-DD\"T\"HH24:MI:SS.MS+05:30') as answer from survey_fact f1 \
join survey_survey s1 on s1.id = f1.survey_id join survey_project p1 on p1.id = s1.project_id \
join survey_surveydesiredfact sdf1 on f1.desired_fact_id = sdf1.desired_fact_id and s1.id = sdf1.survey_id \
join slum_data_household household1 on household1.id = f1.object_id \
where s1.id = %s and p1.id = %s and f1.content_type_id = 27 \
 and household1.slum_id= %s group by household1.household_code) \
UNION All \
(select household.household_code, f.desired_fact_id as question_id, f.data as answer from survey_fact f \
join survey_survey s on s.id = f.survey_id join survey_project p on p.id = s.project_id \
join survey_surveydesiredfact sdf on f.desired_fact_id = sdf.desired_fact_id and s.id = sdf.survey_id \
join slum_data_household household on household.id = f.object_id \
where s.id = %s and p.id = %s and f.content_type_id = 27 and household.slum_id= %s order by household.household_code, sdf.weight asc)"

# since RHS has two survey and its been decided that data from new survey (in case if slum data is in both survey)
# get list of common slum to use data from new slum only
qry_rhs_common_slum_list = "(select distinct household.slum_id from survey_fact f \
join slum_data_household household on household.id = f.object_id \
join survey_survey s on s.id = f.survey_id join survey_project p on p.id = s.project_id \
where s.id = %s and p.id = %s and f.content_type_id = 27 " + run_script_for_selected_slum_household + " order by household.slum_id asc) \
INTERSECT ALL \
(select distinct household.slum_id from survey_fact f \
join slum_data_household household on household.id = f.object_id \
join survey_survey s on s.id = f.survey_id join survey_project p on p.id = s.project_id \
where s.id = %s and p.id = %s and f.content_type_id = 27 " + run_script_for_selected_slum_household + "  \
order by household.slum_id asc)"

# get list of all household in all slums for second survey
qry_rhs_master_slum_household_survey_list = "select distinct household.slum_id, household.household_code from survey_fact f \
join slum_data_household household on household.id = f.object_id \
join survey_survey s on s.id = f.survey_id join survey_project p on p.id = s.project_id \
where s.id = %s and p.id = %s and f.content_type_id = 27  " + run_script_for_selected_slum_household + "  \
order by household.slum_id, household.household_code asc"

# get list of all question and answer for all household in slum from second survey
qry_rhs_master_survey_slum_household_question_answer ="(select household1.household_code, '-1' as question_id, to_char(min(f1.updated_on),'YYYY-MM-DD\"T\"HH24:MI:SS.MS+05:30') as answer from survey_fact f1 \
join survey_survey s1 on s1.id = f1.survey_id join survey_project p1 on p1.id = s1.project_id \
join survey_surveydesiredfact sdf1 on f1.desired_fact_id = sdf1.desired_fact_id and s1.id = sdf1.survey_id \
join slum_data_household household1 on household1.id = f1.object_id \
where s1.id = %s and p1.id = %s and f1.content_type_id = 27 \
 and household1.slum_id= %s group by household1.household_code) \
UNION All \
(select household.household_code, f.desired_fact_id as question_id, f.data as answer from survey_fact f \
join survey_survey s on s.id = f.survey_id join survey_project p on p.id = s.project_id \
join survey_surveydesiredfact sdf on f.desired_fact_id = sdf.desired_fact_id and s.id = sdf.survey_id \
join slum_data_household household on household.id = f.object_id \
where s.id = %s and p.id = %s and f.content_type_id = 27 and household.slum_id= %s order by household.household_code, sdf.weight asc)"

# path of survey excel file(xls) to read option and xml keys
RHS_excelFile = os.path.join(root_folder_path, 'FilesToRead', 'form_RHS_Pune.xls')   # RHS.xls

# create rapid household survey xml
def create_rhs_xml(options):
	# variables
	global question_map_dict
	global question_option_map_dict
	global option_dict
	
	global city_ward_slum_dict
	
	global qry_slum_list
	global qry_rhs_slum_household_survey_list
	global qry_rhs_survey_slum_household_question_answer
	
	global qry_rhs_common_slum_list
	global qry_rhs_master_slum_household_survey_list
	global qry_rhs_master_survey_slum_household_question_answer
	
	global gl_rhs_xml_dict
	
	global RHS_excelFile;
	
	xml_root = options['xml_root']
	xml_root_attr_id = options['xml_root_attr_id']
	xml_root_attr_version = options['xml_root_attr_version']
	xml_formhub_uuid = options['formhub_uuid']
	
	project_id = options['project']
	survey_id = options['survey']
	survey_id2 = options['survey2']
	mapexcelfile = options['mapped_excelFile']
	output_folder_path = options['output_path']
	
	unprocess_records = {}
	
	write_log("Start : Log for RHS Survey for per household in each slum ")
	
	#read old xls file city - ward - slum mapping
	read_xml_excel(RHS_excelFile)
	#print("Read excel file")
	write_log("Read excel file " + RHS_excelFile)
	
	#print(city_ward_slum_dict)
	
	#read map xlsx file for question, option mapping
	read_map_excel(mapexcelfile)
	#print("Read mapped excel file")
	write_log("Read mapped excel file" + mapexcelfile)
	
	# get slum code list
	slum_code_list = {}
	slum_code1_list = get_slum_code(qry_slum_list % survey_id)
	
	# check if second survey is exists or not 
	# get slum code list 
	if survey_id2:
		slum_code2_list = get_slum_code(qry_slum_list % survey_id2)
		
		slum_code2_list.update(slum_code1_list)
		
		slum_code_list.update(slum_code2_list)
	else:
		slum_code_list.update(slum_code1_list)
	
	#print("fatch slum code")
	write_log("fatch slum code")
	
	# set two survey for processing with default values
	rhs_group = {'master':None, 'New':None}
	
	if survey_id2:
		# get common slum among two survey
		common_slum_id_list = get_list_ids(qry_rhs_common_slum_list  % (survey_id, project_id, survey_id2, project_id))
		write_log("fatch common slum in both data for RHS -- " + (', '.join(str(x) for x in common_slum_id_list)))
		
		#print('common_slum_id_list=> ', common_slum_id_list)
		
		master_slum_household_list = get_household_survey(qry_rhs_master_slum_household_survey_list % (survey_id2, project_id))
		#print('master_slum_household_list before - ',master_slum_household_list.keys())
		
		# remove common survey from second survey list
		for slum_id in common_slum_id_list:
			del master_slum_household_list[slum_id]
		
		#print("fetch master slum household list")
		#print('master_slum_household_list  ',master_slum_household_list.keys())
	
		rhs_group['master']= master_slum_household_list
	
	# get slum and household list
	new_slum_household_list = get_household_survey(qry_rhs_slum_household_survey_list % (survey_id, project_id))
	#print("fetch slum household list")
	#print(new_slum_household_list)
	write_log("fetch household slum survey list")

	rhs_group['New'] = new_slum_household_list
	
	total_slum = 0
	unprocess_slum = 0
	
	total_household = 0
	unprocess_household = 0
	
	total_process = 0
	fail = 0
	success = 0
	
	total_process_house = 0
	progess_counter = 0
	slum_survey_date_when_not_available = ''
		
	# check for each survey into group
	for rhs_key, slum_household_list in rhs_group.items():
		#check key value
		#print('rhs_key = ', rhs_key)
		#print('slum_household_list == ',slum_household_list)
		
		# check if data exists for survey
		if slum_household_list:
			# check per household in each slum
			for slum, household_list in slum_household_list.items():
				total_slum += 1
				total_household += len(household_list)
				slum_survey_date_when_not_available = ''
				
				#print("proocessing data for slum - ", slum)
				write_log("proocessing data for slum - "+str(slum))
				
				unprocess_records.setdefault(str(slum), [])
				
				#get slum code for currently processing slum
				try:
					slum_code = None
					slum_code = slum_code_list[slum]
				except:
					pass
				
				# process data only if slum code exists
				if slum_code:
					#get admin ward and city code for slum
					admin_ward = get_slum_wise_admin_ward(slum_code)
					#city = get_city_id(admin_ward)
					
					#print('slum_code : %s  admin_ward : %s  city : %s' % (slum_code, admin_ward, city))
					
					# get query for survey
					qry_rhs_question_answer = ''
					if rhs_key == 'master':
						qry_rhs_question_answer = (qry_rhs_master_survey_slum_household_question_answer  % (survey_id2, project_id, slum, survey_id2, project_id, slum)) 
					else: 
						qry_rhs_question_answer = (qry_rhs_survey_slum_household_question_answer  % (survey_id, project_id, slum, survey_id, project_id, slum))
					
					# get question and answer for households in slum
					household_fact = get_household_wise_question_answer(qry_rhs_question_answer)
					#print(household_fact)
					total_process_house += len(household_fact)
					
					
					
					#For finding the average area for slum to be used if house hold has area as 0
					slum_has_02_current_place_for_defecation_response = False
					total_area_for_slum = 0
					total_household_count_for_average = 0
					average_area_for_slum = 0
					average_area_option_for_slum = '01'
					house_hold_count = 0;
					for household in household_list:
						fact = household_fact[household]
						house_area_in_sq_ft = get_answer('House_area_in_sq_ft', fact)
						current_place_for_defecation = get_answer('Current_place_of_defecation', fact)
						#Find the value for slum date of survey to be used when invalid date is available in the individual record
						if slum_survey_date_when_not_available == '':
							slum_survey_date_when_not_available = get_answer('Date_of_survey', fact)
							if slum_survey_date_when_not_available:
									slum_survey_date_when_not_available = get_formatted_data(slum_survey_date_when_not_available)
									
						if current_place_for_defecation == '02' or (type(current_place_for_defecation) == list and '02' in current_place_for_defecation):
							slum_has_02_current_place_for_defecation_response = True;
						try:
							house_area_in_sq_ft = get_rhs_area_in_squar_feet(house_area_in_sq_ft)
							if type(house_area_in_sq_ft) == list:
								house_area_in_sq_ft = house_area_in_sq_ft[0]
							#print('houise hold wise area:', house_area_in_sq_ft) 
							if house_area_in_sq_ft != 0:
								total_area_for_slum = total_area_for_slum + house_area_in_sq_ft
								total_household_count_for_average += 1
						except:
							#unprocess_records[str(slum)].append([str(household), "unable to process house area in sq ft for answer =>"+(house_area_in_sq_ft if not isinstance(house_area_in_sq_ft, list) else ','.join(house_area_in_sq_ft))])
							pass
					#print('total_area_for_slum:' , total_area_for_slum)		
					#print('total_household_count_for_average:' , total_household_count_for_average)		
					
					if total_household_count_for_average !=0:
						average_area_for_slum = total_area_for_slum / total_household_count_for_average	
					average_area_option_for_slum = get_rhs_area_option_from_squar_feet(average_area_for_slum)
					write_log('Average area option for Slum:' + str(average_area_option_for_slum))
					
					
					
					# set progress bar
					#show_progress_bar(progess_counter, total_process_house, total_slum, len(slum_code_list), 'Slum ' + slum_code)
					print('\nSlum counter:',total_slum)
					# process each household in slum
					for household in household_list:
						total_process += 1
						
						try:
							#print("proocessing data for household - %s in slum - %s" % (household, slum))
							write_log("proocessing data for household - %s in slum - %s" % (household, str(slum)))
							
							#get question and its answers for household
							fact = household_fact[household]
							
							#print('question answer', fact)
							
							# get dictionary to create xml
							rhs_xml_dict = copy.deepcopy(gl_rhs_xml_dict)
							
							# set dictionary to create RHS xml
							rhs_xml_dict['formhub']['uuid'] = xml_formhub_uuid
							
							#rhs_xml_dict['start'] = get_answer('start', fact)
							#rhs_xml_dict['end'] = get_answer('end', fact)
							
							#Direct information without group
							rhs_xml_dict['admin_ward'] = admin_ward
							rhs_xml_dict['slum_name'] = slum_code
							date_of_rhs = get_answer('Date_of_survey', fact)
							write_log('Date of survey:' + str(date_of_rhs))
							if date_of_rhs:
								rhs_xml_dict['Date_of_survey'] = get_formatted_data(date_of_rhs)
							if rhs_xml_dict['Date_of_survey'] == '':
								rhs_xml_dict['Date_of_survey'] = slum_survey_date_when_not_available
								
							#Administrative Information
							#rhs_xml_dict['group_ce0hf58']['city'] = city
							#rhs_xml_dict['group_ce0hf58']['admin_ward'] = admin_ward
							#rhs_xml_dict['group_ce0hf58']['slum_name'] = slum_code

							rhs_xml_dict['Name_s_of_the_surveyor_s'] = get_answer('Name_s_of_the_surveyor_s', fact)
							rhs_xml_dict['Household_number'] = household
							rhs_xml_dict['Parent_household_number'] = get_answer('Parent_household_number', fact)
							
							Type_of_structure_occupancy = get_answer('Type_of_structure_occupancy', fact)
							if Type_of_structure_occupancy and type(Type_of_structure_occupancy) is list:
								Type_of_structure_occupancy = Type_of_structure_occupancy[0]
							if Type_of_structure_occupancy and ' ' in Type_of_structure_occupancy:
								Type_of_structure_occupancy = Type_of_structure_occupancy.split(" ")
								Type_of_structure_occupancy = Type_of_structure_occupancy[0]
							#makeitastring = ','.join(map(str, fact))
							#write_log('Fact value:' + str(fact[440]))
							write_log('Type_of_structure_occupancy value:' + str(Type_of_structure_occupancy))
							#write_log('Data type for type of structure occupency:' + str(type(Type_of_structure_occupancy)))
							if Type_of_structure_occupancy:
								rhs_xml_dict['Type_of_structure_occupancy'] = Type_of_structure_occupancy
							#write_log('After If condition Type_of_structure_occupancy value:' + rhs_xml_dict['Type_of_structure_occupancy'])
							if Type_of_structure_occupancy == '02':
								rhs_xml_dict['Type_of_unoccupied_house'] = get_answer_type_of_unaccopied_house('Type_of_unoccupied_house', fact)
							#print('process - Administrative Information')
							#write_log('process - Administrative Information')
							#********************************This line to be deleted after testing***********************************************
							full_name_of_head_of_household = get_answer('Full_name_of_the_head_of_the_household', fact)
							if full_name_of_head_of_household == 'L H' or full_name_of_head_of_household == 'lh' or full_name_of_head_of_household == 'L.H.' or full_name_of_head_of_household == 'l.h.':
								full_name_of_head_of_household = 'not giving information'
							rhs_xml_dict['group_og5bx85']['Full_name_of_the_head_of_the_household'] = full_name_of_head_of_household
							#********************************This line to be deleted after testing***********************************************
							#Household Information - Personal Information
							if Type_of_structure_occupancy == '01':
								rhs_xml_dict['group_og5bx85']['Full_name_of_the_head_of_the_household'] = get_answer('Full_name_of_the_head_of_the_household', fact)
								rhs_xml_dict['group_og5bx85']['Type_of_survey'] = '01'
								mobile_number_10_digit = get_answer('Enter_the_10_digit_mobile_number', fact)
								if mobile_number_10_digit:
									if type(mobile_number_10_digit) is list:
										mobile_number_10_digit = mobile_number_10_digit[0]
									#This condition to take first mobile number if we have multiple mobile numbers in delimited format 
									if mobile_number_10_digit and len(mobile_number_10_digit) >18:
										if ' ' in mobile_number_10_digit:
											mobile_number_10_digit = mobile_number_10_digit.split(" ")
											mobile_number_10_digit = mobile_number_10_digit[0]
										if ',' in mobile_number_10_digit:
											mobile_number_10_digit = mobile_number_10_digit.split(",")
											mobile_number_10_digit = mobile_number_10_digit[0]
										if '\\' in mobile_number_10_digit:
											mobile_number_10_digit = mobile_number_10_digit.split("\\")
											mobile_number_10_digit = mobile_number_10_digit[0]
										if '/' in mobile_number_10_digit:
											mobile_number_10_digit = mobile_number_10_digit.split("/")
											mobile_number_10_digit = mobile_number_10_digit[0]	
											
									mobile_number_10_digit = mobile_number_10_digit.replace(',', '')
									mobile_number_10_digit = mobile_number_10_digit.replace(',', '')
									mobile_number_10_digit = mobile_number_10_digit.replace(',', '')
									mobile_number_10_digit = mobile_number_10_digit.replace(' ', '')
									#mobile_number_10_digit = mobile_number_10_digit.strip()
									
									if len(mobile_number_10_digit) == 10 and mobile_number_10_digit.isdigit():
										rhs_xml_dict['group_el9cl08']['Enter_the_10_digit_mobile_number'] = mobile_number_10_digit
																		
								aadhar_number_12_digit = get_answer('Aadhar_number', fact)
								if aadhar_number_12_digit:
									if type(aadhar_number_12_digit) is list:
										aadhar_number_12_digit = aadhar_number_12_digit[0]
									aadhar_number_12_digit = aadhar_number_12_digit.replace(', ', '')
									aadhar_number_12_digit = aadhar_number_12_digit.replace(' ,', '')
									aadhar_number_12_digit = aadhar_number_12_digit.replace(',', '')
								if aadhar_number_12_digit and len(aadhar_number_12_digit) == 12 and aadhar_number_12_digit.isdigit():
									rhs_xml_dict['group_el9cl08']['Aadhar_number'] = aadhar_number_12_digit
								
							#print('process - Household Information - Personal Information')
							#write_log('process - Household Information - Personal Information')
							
							#Household Information - General Information
							if Type_of_structure_occupancy == '01':
								what_is_the_structure_of_the_house = get_answer('Type_of_structure_of_the_house', fact)
								if what_is_the_structure_of_the_house:
									rhs_xml_dict['group_el9cl08']['Type_of_structure_of_the_house'] = what_is_the_structure_of_the_house
								
								what_is_the_ownership_status_of_the_house = get_answer('Ownership_status_of_the_house', fact)
								if what_is_the_ownership_status_of_the_house:
									rhs_xml_dict['group_el9cl08']['Ownership_status_of_the_house'] = what_is_the_ownership_status_of_the_house
								write_log('Ownership_status_of_the_house:' + str(what_is_the_ownership_status_of_the_house))
								
								number_of_family_members = get_answer('Number_of_household_members', fact)
								try:
									number_of_family_members = get_rhs_family_member_count(number_of_family_members)
									if int(number_of_family_members) > 20:
										number_of_family_members = 5
									rhs_xml_dict['group_el9cl08']['Number_of_household_members'] = number_of_family_members
								except:
									#unprocess_records[str(slum)].append([str(household), "unable to process number of family member for answer =>"+(number_of_family_members if not isinstance(number_of_family_members, list) else ','.join(number_of_family_members))])
									pass
								write_log('number_of_family_members:' + str(number_of_family_members))
								Do_you_have_a_girl_child_under = get_answer('Do_you_have_any_girl_child_chi', fact)
								if Do_you_have_a_girl_child_under:
									if type(Do_you_have_a_girl_child_under) == list:
										Do_you_have_a_girl_child_under = Do_you_have_a_girl_child_under[0];
									rhs_xml_dict['group_el9cl08']['Do_you_have_any_girl_child_chi'] = Do_you_have_a_girl_child_under
									
									if Do_you_have_a_girl_child_under == '01':
										number_of_girl_child_under_18 = int(get_answer('How_many', fact))
										#If the total member count is less than number of girl chile greater than 18 (this value is reduced to 5 if the value received from survey is greater than 20)
										#then set number of girl child under 18 to number of members count
										if number_of_family_members <= number_of_girl_child_under_18:
											number_of_girl_child_under_18 = number_of_family_members
										if number_of_girl_child_under_18 > 0:	
											rhs_xml_dict['group_el9cl08']['How_many'] = number_of_girl_child_under_18
										else:
											if rhs_xml_dict['group_el9cl08']['Do_you_have_any_girl_child_chi'] == '01':
												rhs_xml_dict['group_el9cl08']['Do_you_have_any_girl_child_chi'] = '02'
								house_area_in_sq_ft = get_answer('House_area_in_sq_ft', fact)
								try:
									house_area_in_sq_ft = get_rhs_area_option_from_squar_feet(house_area_in_sq_ft)
									if type(house_area_in_sq_ft) == list:
										house_area_in_sq_ft = house_area_in_sq_ft[0]
									if house_area_in_sq_ft == 0 or house_area_in_sq_ft == '':
										house_area_in_sq_ft = average_area_for_slum	
									rhs_xml_dict['group_el9cl08']['House_area_in_sq_ft'] = house_area_in_sq_ft
								except:
									#unprocess_records[str(slum)].append([str(household), "unable to process house area in sq ft for answer =>"+(house_area_in_sq_ft if not isinstance(house_area_in_sq_ft, list) else ','.join(house_area_in_sq_ft))])
									pass
								write_log('option for house_area_in_sq_ft:' + str(house_area_in_sq_ft))
								
								rhs_xml_dict['group_oi8ts04']['Have_you_applied_for_individua'] = '02'
								
								Current_place_of_defecation_toilet = get_answer('Current_place_of_defecation', fact)

								has_04_current_place_for_defecation = False
								where_the_individual_toilet_is_connected_to_is_07 = False
								
								if Current_place_of_defecation_toilet:
									if type(Current_place_of_defecation_toilet) == list and '04' in Current_place_of_defecation_toilet:
										has_04_current_place_for_defecation = True
									if type(Current_place_of_defecation_toilet) == list and '01' in Current_place_of_defecation_toilet:
										Current_place_of_defecation_toilet = '01'
									elif type(Current_place_of_defecation_toilet) == list:
										Current_place_of_defecation_toilet = Current_place_of_defecation_toilet[0]		
									#As per discussion done on 17-Apr-2018 if current place of defecation is 05 and corresponding slum has at least one record with current place of defecation as 02 then set value as '02'
									if Current_place_of_defecation_toilet == '05' and slum_has_02_current_place_for_defecation_response:
										Current_place_of_defecation_toilet = '02'
									if Current_place_of_defecation_toilet == '05' and not slum_has_02_current_place_for_defecation_response:
										Current_place_of_defecation_toilet = '10'	
										
									
								
									#As per discussion done on Tuesday 17-Apr-2018
									if has_04_current_place_for_defecation:
										rhs_xml_dict['group_oi8ts04']['OD1'] = '05'
									
									write_log('---------------------value for Current_place_of_defecation_toilet:' + str(Current_place_of_defecation_toilet))
									
									if (Current_place_of_defecation_toilet == '02' or Current_place_of_defecation_toilet == '03' or Current_place_of_defecation_toilet == '06' or Current_place_of_defecation_toilet == '04'):
										rhs_xml_dict['group_oi8ts04']['C2'] = '08'
										rhs_xml_dict['group_oi8ts04']['Current_place_of_defecation'] = '08'
										
									if Current_place_of_defecation_toilet == '01':
										rhs_xml_dict['group_oi8ts04']['C2'] = '05'								
										rhs_xml_dict['group_oi8ts04']['Current_place_of_defecation'] = '05'
									
									if Current_place_of_defecation_toilet == '02':
										rhs_xml_dict['group_oi8ts04']['C3'] = '09'
										rhs_xml_dict['group_oi8ts04']['Current_place_of_defecation'] = '09'										
										
									if Current_place_of_defecation_toilet == '03':
										rhs_xml_dict['group_oi8ts04']['C3'] = '10'
										rhs_xml_dict['group_oi8ts04']['Current_place_of_defecation'] = '10'
									
									if Current_place_of_defecation_toilet == '06':
										rhs_xml_dict['group_oi8ts04']['C3'] = '11'
										rhs_xml_dict['group_oi8ts04']['Current_place_of_defecation'] = '11'			
									
									if Current_place_of_defecation_toilet == '04':
										rhs_xml_dict['group_oi8ts04']['C3'] = '12'
										rhs_xml_dict['group_oi8ts04']['Current_place_of_defecation'] = '12'	
										
									if (Current_place_of_defecation_toilet == '01' or Current_place_of_defecation_toilet == '02'):
										where_the_individual_toilet_is_connected_to_ = get_answer('What_is_the_toilet_connected_to', fact)
										if where_the_individual_toilet_is_connected_to_ == '07':
											where_the_individual_toilet_is_connected_to_is_07 = True
											where_the_individual_toilet_is_connected_to_ = '08'
											rhs_xml_dict['group_oi8ts04']['C3'] = '13'
										if where_the_individual_toilet_is_connected_to_:
											rhs_xml_dict['group_oi8ts04']['What_is_the_toilet_connected_to'] = where_the_individual_toilet_is_connected_to_
								
								type_of_water_connection = get_answer('Type_of_water_connection', fact)
								if type_of_water_connection:
									rhs_xml_dict['group_el9cl08']['Type_of_water_connection'] = type_of_water_connection
								write_log('Type_of_water_connection:' + str(type_of_water_connection))
								
								facility_of_waste_collection = get_answer('Facility_of_solid_waste_collection', fact)
								if facility_of_waste_collection:
									if type(facility_of_waste_collection) == list:
										facility_of_waste_collection = facility_of_waste_collection[0]
									rhs_xml_dict['group_el9cl08']['Facility_of_solid_waste_collection'] = facility_of_waste_collection
								
								if not where_the_individual_toilet_is_connected_to_is_07 and Current_place_of_defecation_toilet and (Current_place_of_defecation_toilet != '01'):
									Are_you_interested_in_individu = get_answer('Are_you_interested_in_an_indiv', fact)
									if Are_you_interested_in_individu:
										if type(Are_you_interested_in_individu) == list:
											Are_you_interested_in_individu = Are_you_interested_in_individu[0]
										if Are_you_interested_in_individu == '01' or Are_you_interested_in_individu == '02':
											rhs_xml_dict['group_oi8ts04']['Are_you_interested_in_an_indiv'] = Are_you_interested_in_individu
										else:
											write_log('Are_you_interested_in_an_indiv:' + Are_you_interested_in_individu)
										
										if Are_you_interested_in_individu == '01':
											if_yes_why_ = get_answer('If_yes_why', fact)
											if if_yes_why_:
												rhs_xml_dict['group_oi8ts04']['If_yes_why'] = if_yes_why_
											
										if Are_you_interested_in_individu == '02':
											if_no_why_ = get_answer('If_no_why', fact)
											if if_no_why_:
												rhs_xml_dict['group_oi8ts04']['If_no_why'] = if_no_why_
										
										if Are_you_interested_in_individu == '01':
											type_of_toilet_preference = get_answer('What_kind_of_toilet_would_you_like', fact)
											if type_of_toilet_preference:
												rhs_xml_dict['group_oi8ts04']['What_kind_of_toilet_would_you_like'] = type_of_toilet_preference
												if type_of_toilet_preference == '05' and (Are_you_interested_in_individu == '01' or Are_you_interested_in_individu == '02') and (if_yes_why_ == '' and if_no_why_ == ''):
													rhs_xml_dict['group_oi8ts04']['If_yes_why'] = '08'
													rhs_xml_dict['group_oi8ts04']['If_no_why'] = '08'
								
								if rhs_xml_dict['group_oi8ts04']['OD1'] != '05':
									rhs_xml_dict['group_oi8ts04']['OD1'] = '01'	
								#if Current_place_of_defecation_toilet and Current_place_of_defecation_toilet != '01':
								#	Have_you_applied_for_indiviual = get_answer('Have_you_applied_for_indiviual', fact)
								#	if Have_you_applied_for_indiviual:
								#		rhs_xml_dict['group_ye18c77']['grup_yw8pj39']['Have_you_applied_for_indiviual'] = Have_you_applied_for_indiviual
										
								#		if Have_you_applied_for_indiviual == '01':
								#			How_many_installements_have_yo = get_answer('How_many_installements_have_yo', fact)
								#			if How_many_installements_have_yo:
								#				rhs_xml_dict['group_ye18c77']['group_yw8pj39']['How_many_installements_have_yo'] = How_many_installements_have_yo
								#				
								#				if How_many_installements_have_yo == '02' or How_many_installements_have_yo == '03':
								#					rhs_xml_dict['group_ye18c77']['group_yw8pj39']['when_did_you_receive_the_first_installment_date'] = get_answer('when_did_you_receive_the_first_installment_date', fact)
								#				
								#				if How_many_installements_have_yo == '03':
								#					rhs_xml_dict['group_ye18c77']['group_yw8pj39']['when_did_you_receive_the_second_installment_date'] = get_answer('when_did_you_receive_the_second_installment_date', fact)
								#			
								#			what_is_the_status_of_toilet_under_sbm_ = get_answer('what_is_the_status_of_toilet_under_sbm_', fact)
								#			if what_is_the_status_of_toilet_under_sbm_:
								#				rhs_xml_dict['group_ye18c77']['group_yw8pj39']['what_is_the_status_of_toilet_under_sbm_'] = what_is_the_status_of_toilet_under_sbm_
								#
								
								#Does_any_family_members_has_co = get_answer('Does_any_family_members_has_co', fact)
								#if Does_any_family_members_has_co:
								#	rhs_xml_dict['group_ye18c77']['group_yw8pj39']['Does_any_family_members_has_co'] = Does_any_family_members_has_co
							
							#print('process - Household Information - General Information')
							#write_log('process - Household Information - General Information')
							
							rhs_xml_dict['Enter_household_number_again'] = household
							
							rhs_xml_dict['__version__'] = xml_root_attr_version
							
							rhs_xml_dict['meta']['instanceID'] = 'uuid:' + str(uuid.uuid4())
							
							
							# get xml string to store in xml file
							repeat_dict = {}
							xml_root_string = create_xml_string(rhs_xml_dict, repeat_dict, xml_root, xml_root_attr_id, xml_root_attr_version)
							
							# create xml file
							file_name = 'RHS_Survey_Slum_Id_' + str(slum) + '_House_code_' + household
							
							final_output_folder_path = os.path.join(output_folder_path, "slum_" +str(slum))
							
							create_xml_file(xml_root_string, file_name, final_output_folder_path)
							
							success += 1
								
							#print ('rhs data - ', rhs_xml_dict)
							
							del rhs_xml_dict
							
							#break;
						except Exception as ex:
							exception_log = 'Exception occurred for household id ' +str(household) + ' of slum id ' + str(slum) + ' \t  exception : '+ str(ex) +' \t  traceback : '+ traceback.format_exc()
							unprocess_records[str(slum)].append([str(household), str(ex)])
							
							fail += 1
							write_log(exception_log)
							
							#break;
							pass
							
						progess_counter += 1
						show_progress_bar(progess_counter, total_process_house, total_slum, len(slum_code_list), 'Slum ' + slum_code)
					#break;
				else:
					unprocess_slum += 1
					
					# write log that slum code is not found for slum id
					write_log('slum code is not found for slum id '+str(slum))
					unprocess_records[str(slum)].append([None, 'slum code is not found when mapped'])
			#break;
			
			
	if unprocess_records:
		write_log('List of slum and household for which unable to create xml')
		write_log('slum_id \t household_code \t exception')
		for slum_id, error_lst in unprocess_records.items():
			for error in error_lst:
				#print('error ', error[0], '    msg ',error[1])
				write_log(slum_id+' \t\t' + (error[0]+' \t' if error[0] else ' \t\t') +' \t\t\t' + error[1])
		
	write_log('End : Log for RHS Survey for slum \n')
	print("End processing")
	
	set_process_slum_count(total_slum, unprocess_slum)
	set_process_household_count(total_household, unprocess_household)
	set_process_count(total_process, success, fail)
	show_process_status()
	
	return;



