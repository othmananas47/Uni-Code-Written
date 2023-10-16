def stock_getter(Ticker,start_date,end_date):
    yf.pdr_override()
    return yf.download(Ticker,start_date,end_date) #pdr.get_data_yahoo(Ticker,start=start_date,end=end_date)

def call_api_with(url_extension):
    your_company_house_api_key ="d125fe41-a8cc-4ec8-9120-a699dc9b887b"
            
    login_headers = {"Authorization":your_company_house_api_key}
    url = f"https://api.companieshouse.gov.uk/{url_extension}"
    # above: could be eg. https://api.companieshouse.gov.uk/search/companies?q=shop&items_per_page=1
    print(f'requesting: {url}') 
    # above, optional: printing, so that you see visually how many calls you are making
    res = requests.get(url, headers=login_headers) #, verify=False)
    return res.json()

def get_one_test_company_or_error():
    url = f"search/companies?q=shop&items_per_page=1"
    return call_api_with(url)


def search_for_companies_with_query(query, number_of_companies = 100):
    # for simplicity round up the number of returned companies to the nearest hundred. eg. 130 becomes 200
    page_size = 100
    number_of_pages = math.ceil(number_of_companies / page_size) # round up
    companies = []
    for page_index in range(0, number_of_pages):
        url = f"search/companies?q={query}&items_per_page={page_size}&index_start={page_index*page_size}"
        companies += call_api_with(url).get('items', [])
    return companies

def data_for_company(company_number):
    url = f"company/{company_number}"
    return call_api_with(url)


def all_persons_in_company(company_number):
    url = f"company/{company_number}/persons-with-significant-control"
    return call_api_with(url).get('items', [])


def filing_history(company_number,number_of_filings=100):
    page_size = 100
    number_of_pages=5
    filhistpage=[]
    url = f"company/{company_number}/filing-history?category=capital&items_per_page=500"
    return call_api_with(url)

def detailed_info_about_companies_with_ids(companies_numbers):
    results = []
    for company_number in companies_numbers:
        results.append(data_for_company(company_number))
    return results

def detailed_info_about_companies_with_name(name, how_many = 12):
    # eg. unless otherwise stated, just grab 10 companies detailed info
    companies_basic_info = search_for_companies_with_query(name, how_many)
    companies_ids = [company['company_number'] for company in companies_basic_info]
    companies = detailed_info_about_companies_with_ids(companies_ids[:how_many])
    return companies

def public_limited_company_checker(list_of_companies):
    plc_count = 0 
    for company in list_of_companies:
        if "PLC" in company['company_name']:
            plc_count+=1
            public_limited_company = company
            
    if plc_count == 0:
        raise Exception("None of the Companies in the List contained PLC")
    
    return public_limited_company 


def updated_public_limited_company_checker(list_of_companies):
    plc_count = 0 
    for company in list_of_companies:
        name_of_company_as_string = company['company_name']
        name_of_company_without_punctuation = name_of_company_as_string.translate(str.maketrans('','',string.punctuation))
        if "PLC" in name_of_company_without_punctuation:
            plc_count+=1
            public_limited_company = company
            
    if plc_count == 0:
        raise Exception("None of the Companies in the List contained PLC")
    
    return public_limited_company 

bp_plc = updated_public_limited_company_checker(bp_companies)


def filing_history(company_number,number_of_filings=100):
    url = f"company/{company_number}/filing-history?category=capital&items_per_page={number_of_filings}"
    return call_api_with(url)


def share_cancellations_extractor(filing_history):
    filing_history_as_list = [value_from_key for value_from_key in filing_history.values()]
    for value_from_key in filing_history_as_list:
        if type(value_from_key)== list:
            filing_history_data = value_from_key
    share_cancellations = []
    for filing_history_element in filing_history_data:
        if ('description', 'capital-cancellation-shares') in filing_history_element.items():
            share_cancellations.append(filing_history_element)
    date_and_values=[]
    for cancellation in share_cancellations:
        action_date = cancellation.get('action_date')
        filing_date = cancellation.get('date')
        capital = cancellation.get('description_values').get('capital')
        value_of_cancellation = []
        for share_type in capital:
            currency = share_type.get('currency')
            figure = share_type.get('figure')
            currency_figure = (currency,figure)
            value_of_cancellation.append(currency_figure)
        if value_of_cancellation[0][0]=='GBP':
            value_of_cancellation.reverse()
        if len(value_of_cancellation)==2:
            date_currency_figure = (action_date,filing_date,value_of_cancellation[0],value_of_cancellation[1])
        else: 
            date_currency_figure = (action_date,filing_date,value_of_cancellation[0],0)
        date_and_values.append(date_currency_figure)
        
    return date_and_values


def time_frame(list_of_dataframes):
    time_frame_list=[]
    for company in list_of_dataframes:
        first_date_as_string = company.iloc[0].at['Action Date']
        last_date_as_string = company.iloc[-1].at['Action Date']
        first_date = datetime.strptime(first_date_as_string, "%Y-%m-%d")
        last_date = datetime.strptime(last_date_as_string, "%Y-%m-%d")
        difference = first_date-last_date
        time_frame_list.append(difference)
    return time_frame_list


def data_up_until_year(data,year):

    
    returned_data = data.copy()
    cut_off_point = len(returned_data)
    for index_count in range(len(data)):
        date_in_iteration = data.iloc[index_count].at['Action Date']
        date_in_iteration_as_string = datetime.strptime(date_in_iteration, "%Y-%m-%d")
        if date_in_iteration_as_string.year == year:
            cut_off_point = index_count
            break

    if cut_off_point ==len(returned_data):
        return returned_data
    else:
        return returned_data.iloc[:cut_off_point]


def stock_getter(Ticker,start_date,end_date):
    yf.pdr_override()
    return yf.download(Ticker,start_date,end_date)

def year_to_date_percentage_gain(dataframe):
    ## requires a dataframe of stock prices
    # first close minus last close divided by first close. 
    first_close = dataframe.iloc[0].at["Close"]
    last_close = dataframe.iloc[-1].at["Close"]
    percentage_gain = (last_close-first_close)/first_close
    
    return percentage_gain


def officers(company_number,number_of_persons=100):
    url = f"company/{company_number}/officers"
    return call_api_with(url)


def officer_extractor(raw_data):
    raw_data_as_list = [value for value in raw_data.values()]
    for dictionary_element in raw_data_as_list:
        if type(dictionary_element)==list:
            officer_data = dictionary_element
    officers_in_company = []
    for officer_element in officer_data:
        name = officer_element.get('name')
        role = officer_element.get('officer_role')
        date_appointed = officer_element.get('appointed_on')
        nationality = officer_element.get('nationality')
        date_of_birth = officer_element.get('date_of_birth')
        country_of_residence = officer_element.get('country_of_residence','England')
        occupation = officer_element.get('occupation')
        resignation_date = officer_element.get('resigned_on','Still Working Here')
        
        #Here we do some data manipulation to create new properties
        if date_appointed != None:
            date_appointed_datetime = datetime.strptime(date_appointed,"%Y-%m-%d")
        if resignation_date != 'Still Working Here':
            last_day_at_company_datetime = datetime.strptime(resignation_date,"%Y-%m-%d")
        elif resignation_date == 'Still Working Here':
            last_day_at_company_datetime = datetime.now()
        time_at_company = math.floor((last_day_at_company_datetime-date_appointed_datetime).days)
        
        if date_of_birth != None:
            date_birth_year = str(date_of_birth.get('year'))
            date_birth_month = str(date_of_birth.get('month'))
            date_of_birth_as_string = date_birth_year +'-'+date_birth_month
            date_of_birth_as_datetime = datetime.strptime(date_of_birth_as_string,"%Y-%m")
            age = (math.floor((datetime.now()-date_of_birth_as_datetime).days/365))
            date_of_birth = date_of_birth_as_datetime
        else:
            age = "Unknown"
            
        if time_at_company < 0:
            time_at_company = 0
        officer_entry = [name,
                        role,
                        date_appointed,
                        nationality,
                        date_of_birth,age,
                        country_of_residence,
                        occupation,
                        resignation_date,time_at_company]
        officers_in_company.append(officer_entry)
        
    return officers_in_company


def nationality_statistics(data):
    nationality_list =[]
    for index,row in data.iterrows():
        if row['Nationality'] not in nationality_list:
            nationality_list.append(row['Nationality'])
            
    nationality_counter = nationality_list.copy()

    for nationality_index in range(len(nationality_list)):
        days_at_company_for_nationality=0
        count =0
        for index,row in (data).iterrows():
            if row['Nationality'] == nationality_list[nationality_index]:
                days_at_company_for_nationality+= int(row['Days at Company'])
                count+=1
        nationality_counter[nationality_index]=(nationality_counter[nationality_index],days_at_company_for_nationality/count,count)
        
    nationality_counter_dataframe = pd.DataFrame(nationality_counter).set_index(pd.Index(nationality_list))
    nationality_counter_dataframe.columns = ["Nationality","Average Days at Company","Number of People"]
    
    for index,row in nationality_counter_dataframe.iterrows():
        if row['Average Days at Company']==0:
            nationality_counter_dataframe = nationality_counter_dataframe.drop(labels=index,axis=0)
    
    
    
    return nationality_counter_dataframe



def residence_statistics(data):
    residence_list=[]
    for index,row in data.iterrows():
        if row['Residence'] not in residence_list:
            residence_list.append(row['Residence'])
            
    residence_counter = residence_list.copy()

    for residence_index in range(len(residence_list)):
        days_at_company_for_residence=0
        count =0
        for index,row in (data).iterrows():
            if row['Residence'] == residence_list[residence_index]:
                days_at_company_for_residence+= int(row['Days at Company'])
                count+=1
        residence_counter[residence_index]=(residence_counter[residence_index],days_at_company_for_residence/count,count)
        
    residence_counter_dataframe = pd.DataFrame(residence_counter).set_index(pd.Index(residence_list))
    residence_counter_dataframe.columns = ["Residence","Average Days at Company","Number of People"]
    return residence_counter_dataframe
