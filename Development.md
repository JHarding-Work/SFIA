## Risk Assessment
### Sensitive information
- Names from the person model.
- Card information.
- Address information.

Database server should be kept in a standalone instance without any publicly accessible ports. 
Router should be equipped with a firewall to block malicious traffic.


### Passwords
- Passwords should be hashed in the database so in the event the database gets compromised
a malicious action wouldn't be able to use it to log into that database
- Passwords should use a salt so that duplicate passwords will not be identifiable across the 
database.


### Access Credentials
Any sort of authentication details should be kept as environment details in the jenkins credentials.


### Copyright
Because we are using this for educational use, we are permitted to use copyright protected images
in the project. This is to verify the images are correctly loading on the page.
