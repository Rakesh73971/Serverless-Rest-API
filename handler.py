import json
import os
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime


def send_email(event, context):
    """
    AWS Lambda function to send email using SendGrid
    
    Expected input:
    {
        "receiver_email": "recipient@example.com",
        "subject": "Email Subject",
        "body_text": "Email body content"
    }
    """
    
    # Initialize SendGrid client
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        return create_response(500, {
            'success': False,
            'error': 'Server configuration error',
            'message': 'SENDGRID_API_KEY environment variable is not configured'
        })
    
    sg = SendGridAPIClient(api_key=sendgrid_api_key)
    
    try:
        # Parse the request body
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return create_response(400, {
                'success': False,
                'error': 'Invalid JSON in request body',
                'message': 'Request body must be valid JSON'
            })
        
        # Extract required fields
        receiver_email = body.get('receiver_email')
        subject = body.get('subject')
        body_text = body.get('body_text')
        
        # Validate required fields
        if not receiver_email:
            return create_response(400, {
                'success': False,
                'error': 'Missing required field',
                'message': 'receiver_email is required'
            })
        
        if not subject:
            return create_response(400, {
                'success': False,
                'error': 'Missing required field',
                'message': 'subject is required'
            })
        
        if not body_text:
            return create_response(400, {
                'success': False,
                'error': 'Missing required field',
                'message': 'body_text is required'
            })
        
        # Validate email format
        if not is_valid_email(receiver_email):
            return create_response(400, {
                'success': False,
                'error': 'Invalid email format',
                'message': 'receiver_email must be a valid email address'
            })
        
        # Check if FROM_EMAIL is configured
        from_email = os.environ.get('FROM_EMAIL')
        if not from_email:
            return create_response(500, {
                'success': False,
                'error': 'Server configuration error',
                'message': 'FROM_EMAIL environment variable is not configured'
            })
        
        # Create SendGrid Mail object
        message = Mail(
            from_email=from_email,
            to_emails=receiver_email,
            subject=subject,
            plain_text_content=body_text
        )
        
        # Send email using SendGrid
        response = sg.send(message)
        
        # Return success response
        return create_response(200, {
            'success': True,
            'message': 'Email sent successfully',
            'messageId': response.headers.get('X-Message-Id', 'unknown'),
            'data': {
                'receiver_email': receiver_email,
                'subject': subject,
                'sent_at': datetime.utcnow().isoformat() + 'Z'
            }
        })
        
    except Exception as e:
        print(f"SendGrid Error: {str(e)}")
        
        # Handle specific SendGrid errors
        if hasattr(e, 'body') and e.body:
            try:
                error_data = json.loads(e.body)
                error_message = error_data.get('errors', [{}])[0].get('message', 'Unknown SendGrid error')
            except:
                error_message = str(e)
        else:
            error_message = str(e)
        
        # Handle common SendGrid error scenarios
        if 'unauthorized' in error_message.lower():
            return create_response(401, {
                'success': False,
                'error': 'Authentication error',
                'message': 'Invalid SendGrid API key'
            })
        
        if 'forbidden' in error_message.lower():
            return create_response(403, {
                'success': False,
                'error': 'Permission error',
                'message': 'SendGrid API key does not have required permissions'
            })
        
        if 'bad request' in error_message.lower() or 'invalid' in error_message.lower():
            return create_response(400, {
                'success': False,
                'error': 'Invalid request',
                'message': f'SendGrid error: {error_message}'
            })
        
        # Generic SendGrid error response
        return create_response(500, {
            'success': False,
            'error': 'SendGrid service error',
            'message': f'SendGrid error: {error_message}'
        })
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return create_response(500, {
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred while sending the email'
        })


def is_valid_email(email):
    """
    Validate email format using regex
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def create_response(status_code, body):
    """
    Create HTTP response with proper headers
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps(body)
    }
