# Pre-deployment tests automation guide

# Pre-requisites:

- Python 3.10.6 or higher
- Google Chrome
- VS code
- SSH

# Modules:

- selenium
- json
- logging
- time

Those can be installed by using the command "pip install <name_of_the_module>" in the VS code terminal. The order does not matter.

Example:

```jsx
pip install selenium
```

# Setup:

The test data used in all the tests are stored in the file "credentials.json". It is recommended that you modify the credentials to your own, but you can also use my client. Below are the fields that you should modify:

```

    "testEmail": "*",
    "testPhone": "*",
    "testCPF": "*",
    "testFirstName": "Leonardo",
    "testLastName": "Menegon",
    "testAddressNumber": "*",
    "testComplementNumber": "*"
```

Before executing the tests it is important to clear the data from all tables, if we are executing tests related to Prospects, we can do that with the following query:

```sql
create temp table variables
   (
      email varchar(80),
      id_number varchar(80),
      cell varchar(80)
   );

insert into variables
values ('','',''); -- <<<< modify this to reflect your own email, cpf and phone number.

delete from identity_management.users_roles
where user_id = (select id from identity_management.users where lower(email) = lower((select email from variables)));

delete from identity_management.users 
where lower(email) = lower((select email from variables));

delete from client_management.clients
where cell_phone_number = (select cell from variables) or lower(email) = lower((select email from variables)) or id_number = (select id_number from variables);

delete from  kyc.prospects
where "data" -> 'personalInfo' ->> 'idNumber' = (select id_number from variables);

delete from kyc.clients
where cell_phone_number = (select cell from variables) or lower(email) = lower((select email from variables)) or person_id_number = (select id_number from variables);

delete from kyc.applications
where "data" -> 'prospect' -> 'cellPhoneNumber' ->> 'value' = (select cell from variables) or lower("data" -> 'prospect' -> 'email' ->> 'value') = lower((select email from variables)) or "data" -> 'prospect' -> 'personId' -> 'number' ->> 'value' = (select id_number from variables);

delete from kyc.phone_blacklist
where cell_phone_number = (select cell from variables);

delete from kyc.blacklisted_documents
where id_number = (select id_number from variables);

delete from originations_v2.applications
where national_id_number = (select id_number from variables);

delete from originations_v2.client_autopayment 
where client_id = (select id from originations_v2.client_status where national_id_number = (select id_number from variables));

delete from channels.orders 
where client_national_id_number in (select id_number from variables);

delete from originations_v2.client_status 
where national_id_number = (select id_number from variables) or "data" -> 'cellPhone' ->> 'number' = (select cell from variables) or lower("data" -> 'email' ->> 'address') = lower((select email from variables));

drop table variables;
```

# Execution:

After doing that the execution of the script is simple. Just type for example:

```python
python [payLinkClient.py](http://paylinkclient.py/)
```

This will open a new private google chrome tab and the script will start.
For now, the tests require manual input on the following scenarios:

- payLink that is sent to the test email
- OTP code that is sent to the test cellPhone
- payment of the QR code - waiting for it to be automatically paid also works, or use stark bank to complete it faster

For paylink and OTP codes, the test will ask you in the console to input the link or otp code, simply paste it there and press enter and let the process continue. Example of paylink and otp input:


Every time you execute a test, a log file will be created with the information regarding the test. If the test for some reason fails it is smart enough to re-try the test, however it will always start from the beginning.