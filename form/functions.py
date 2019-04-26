#function for calculating the total amount of a material. Takes in a queryset from the MaterialsModel.
#Returns the sum of all quantity entries from a particular queryset.
def calculate_total_materials(q_set):
    sum = 0
    for entry in q_set:
        sum += int(entry.quantity)
    return sum


#class for a material. Contains its material name and quantity
class Material(object):
    def __init__(self, material_type, quantity):
        self.m = material_type
        self.q = quantity


#function that determines the schedules for each employee. Could be made more efficient, as it runs two for loops.
def determine_schedules(clock_in, clock_out):
    schedule_list = []

    for ci in clock_in:
        for co in clock_out:
            if ci.employee_name == co.employee_name and ci.date_submitted == co.date_submitted:
                schedule_list.append(
                    "Employee Name: " + ci.employee_name + 
                    '\nTime arrived: ' + ci.time_arrived.strftime('%Y-%m-%d %H:%M') +
                    '\nTime departed: ' + co.time_departed.strftime('%Y-%m-%d %H:%M'))
                break
            else: 
                pass
    return schedule_list