def main(event, context):

    if event["triggerSource"] == "CustomMessage_SignUp":

        code = event["request"]["codeParameter"]
        email = event["request"]["userAttributes"]["email"]

        verify_link = f"https://d3cfmp200ge6w8.cloudfront.net/verifyPage?email={email}&code={code}"

        event["response"]["emailSubject"] = "Grammy Account Verification"

        event["response"]["emailMessage"] = f"""
        <h2>Account Verification</h2>
        <p>Your verification code:</p>
        <h1>{code}</h1>

        <p>Or to verify your account, click this link:</p>
        <a href="{verify_link}">Verify your account</a>
        """

    return event