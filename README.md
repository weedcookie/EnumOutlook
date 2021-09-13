# OutlookBrute
A script to brute force outlook emails 

<p>Below is part of the html to in the response that tells us if the email is valid or not </p>

```
	# if value is 1 user is invalid 
	reg = r'IfExistsResult\":1'

	## if value is 0 then user is valid 
	reg2 = r'IfExistsResult\":0'```




Setup :
```
pip3 install -r req.txt
```

Usage:
```
python3  master_.py [-h] [-s S] [-m M] [-g G] [-g2 G2] [-t T]

optional arguments:
  -h, --help  show this help message and exit
  -s S        single email check
  -m M        multiple email check
  -g G        generate and check without user interference
  -g2 G2      generate and check without user interference
  -t T        threaded
     
```

PS : g uses names module to generate first name only 
     g2 uses random-username module to generate custom username
     
