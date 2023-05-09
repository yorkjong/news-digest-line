"""
This module is for minicing Vercel environment.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/07 (initial version) ~ 2023/05/08 (last revision)"

import os


def init_environ_variables():
    print('init_environ_variables')

    os.environ['SERVICE_ACCOUNT_INFO'] = r'''
    {
      "type": "service_account",
      "project_id": "gdrive-385220",
      "private_key_id": "bbf6a9541a513c63ff55ebf6502a1b282d896888",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC501oT5o38MrHF\nKWLlA0us0CNKeF7OR/y++rnCAs2wR0OsVRuB9+I7H5zTRP+kAKam8ij8dMAEnSHk\nmEmO46hGGIDQTCg/TXiwIF/nzkmEo8aTcJNjOIB70Sx+y7sx8KAxc178BVnv5J8m\ndEtm4tXRdIFKXY4bVSJEMgQ58Z7LiPc+pGwFsHEc+f9eT9yUrFK9dqs1Mx5U7p79\ncOtM1IgbjIE7mxDAXl9YUWQrXV8QM73zhb9KQV1PZZF5L66RGZiDSEhvTToeYVXR\nB7uxfOoLTqsXOQ7P3/BXRIIFlJgDaNhLh2iORz0TEUxjdlb3JypVvb5kmnYkKnQG\nA8M6qVOpAgMBAAECggEAAuLvkUORjQtUi5V6/cexUzvgcHWyM04W9Ph8DjFw9H4G\n5RRlWv14vCZfj0CRIAEKlalJTbKakPfH4P8klV2f7YbP6Wxla6ZOa531H2qq5a6N\nlRi4kV/9Tu8O2+FaRQpR0rLSFOQYY4uPlU9VJIH9hEVlBLyzSmVmJN0KB8RjDRJK\nuqJLrr+udK6+1pDzBal3gKs4iGzaizJEbUypvPqp/UmNtIwfiUfpBcE5fLMvl9+w\neRLPx/ENBe7/N0z8iukgYU1g1pB7qqoMD7lAeuFEeb4NgY1v0FhWLpYpegjOu1Og\nIsZmrYLOgRAyy9JeK8ExmXw4YiScf+zy1dUR8iA2AQKBgQD9d1FToiOI3xzvhpFK\not5eurljODw7oYQ4nS+wtrR7tnntr4/9fwjsAImpn9U/EiN3YLukSfMihPdPBOSj\nSKL0xguaIYFnF6itJZOHxxSeu2UBAj9kh0vOjTeaRPFhFOoUfqWCVjYTWpXV4btr\naDDvqTCbYuOOWQoJRD3viI7yyQKBgQC7ruzq3GroJm0GdbkkJfzv8/jUZjwMbs+W\nQ9DPjHfSELFCC1T8xb9+/rJK6OkeuFWYXKavLl4U0nkJCyBVPfwZUiuLnW64laFX\nP/73BqLMUMkpbUG+9Y32zn2Mq3E66+P+CpwglT3r5A/eG9eXCFTyFDQl7tr0vC1N\nY77XayXp4QKBgQCC0a9+6+NNRGJp2dlpXTBKUjNW23JzEITut2oi2dnDNEYv//ng\nS02uiQSEMMNePx1hAuM2AxjjCx+dgBgFknrQvNrGHV7td4+OdiNz47Nnza5u29se\nJppgrBAzpjuy8Jl0JH2GDLryOEG3Vz9lSyxetcMpn9t0383HRJp249NryQKBgQCf\n4P+JgoK/iBxP6HDyzjmN3vMVXJHCtZK4msSCSVK46+dUL3sSaRIcCLOxBH+x361q\nwWJs0L7sVe8tOQEuHENo/oqBwHbVXwG15Zo4rLp5+keitqPPHDb3DCf/cPxgCRqL\nCla9muTI0dqCho0856gVIAjcV4DGApdE2bd0op4FgQKBgF0c/9bKvW3sISFVEGpB\nBP4IK+EqMNB8mdwBgD1Fzlq8EpjHhbyG8N7MwOn/betWhjWJ5LmwC/FgNXlWgd4U\nVHcME5iI3xHMb0wYLGFY3N41+108JZvsC4dky72c1iR5oAk56b0MFF8ZjGUolh33\nSrJYsGzT9y8tTBb15k33k0tT\n-----END PRIVATE KEY-----\n",
      "client_email": "news-digest@gdrive-385220.iam.gserviceaccount.com",
      "client_id": "101728028730105787803",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/news-digest%40gdrive-385220.iam.gserviceaccount.com"
    }
    '''

    os.environ['FOLDER_ID'] = '17Ha4asx9zjPb2UI6tvQP1ofs2f166kUR'

