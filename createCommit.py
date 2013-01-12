import urllib
import urllib2

# use json in Python 2.7, fallback to simplejson for Python 2.5
try:
    import json
except ImportError:
    import simplejson as json

GITHUB_URL = "https://api.github.com"
BASE_URL = GITHUB_URL + "/repos/alfonsodev/testGithubApi"
TOKEN = "966dff7274bb5aab564ee7783d3b59761fced116"
authHeader = {'Authorization': 'token ' + TOKEN, 'Content-Type': 'application/json'}
# class urllib2.Request(url[, data][, headers][, origin_req_host][, unverifiable])

# Store latest commit SHA
request = urllib2.Request(BASE_URL + '/git/refs/heads/master', headers = authHeader )
response = urllib2.urlopen(request)
rawJson = response.read()
gitRefs = json.loads(rawJson)
latestCommitSha = gitRefs['object']['sha']

# Store latest commit tree SHA
request = urllib2.Request(BASE_URL + '/git/commits/' + latestCommitSha , headers = authHeader )
response = urllib2.urlopen(request)
rawJson = response.read()
jsonCommit = json.loads(rawJson)
treeSha = jsonCommit['tree']['sha']

# Create a new tree
jsonString = '{ "tree": [\
    {\
        "base_tree": "' + treeSha + '",\
        "path": "autoCommitedFile.txt",\
        "mode": "100644",\
        "type": "blob",\
        "sha": "' + treeSha + '"\
        "content:"this file was commited via github api"\
    }\
  ]\
}\
'
request = urllib2.Request(BASE_URL + '/git/trees/', json.dumps(jsonString), headers = authHeader )
response = urllib2.urlopen(request)
rawJson = response.read()
jsonNewTree = json.loads(rawJson)
newTreeSha = jsonNewTree['sha']


# Create a new commit
# POST /repos/:user/:repo/git/commits while authenticated

# print "newTreeSha:" + newTreeSha

print treeSha
print latestCommitSha
