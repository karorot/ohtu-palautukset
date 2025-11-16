*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  pekka
    Set Password  pekka123
    Set Password Confirmation  pekka123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  pe
    Set Password  pekka123
    Set Password Confirmation  pekka123
    Click Button  Register
    Register Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  pekka
    Set Password  pe1
    Set Password Confirmation  pe1
    Click Button  Register
    Register Should Fail With Message  Password must be at least 8 characters long

Register With Valid Username And Invalid Password
    Set Username  pekka
    Set Password  pekkapassword
    Set Password Confirmation  pekkapassword
    Click Button  Register
    Register Should Fail With Message  Password must contain at least one number

Register With Nonmatching Password And Password Confirmation
    Set Username  pekka
    Set Password  pekka123
    Set Password Confirmation  pekka456
    Click Button  Register
    Register Should Fail With Message  Password and password confirmation do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle456
    Set Password Confirmation  kalle456
    Click Button  Register
    Register Should Fail With Message  Username is already taken

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page