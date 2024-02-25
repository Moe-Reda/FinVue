class CreateSavings:
    
    def createSavings(self, initial, monthly, ir, time_period):
        try:
            month_counter = 0
            monthly_ir = ir/12
            savings_list = []
            savings_list.append({'datapoint': initial, 'month': month_counter})
            while month_counter < time_period:
                month_counter += 1
                fv = (initial * ((1+monthly_ir)**month_counter)) + (monthly*((((1+monthly_ir)**month_counter)-1)/monthly_ir))
                savings_list.append({'datapoint': fv , 'month': month_counter})
                

            return savings_list, 200
        except Exception as e:
            return {'error': str(e)}, 500