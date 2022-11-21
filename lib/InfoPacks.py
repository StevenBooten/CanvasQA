def getStatusCode(code):
    
    statusCode = {
                '0' : "The Link checker has failed, most likely due to SSO issues or it's a file which is shared with specific people. This link is likely okay.",
                '100': "Continue. This means that the server in question has received your browser\'s request headers, and is now ready for the request body to be sent as well. This makes the request process more efficient since it prevents the browser from sending a body request even though the headers have been rejected.",
                '101': "Switching protocols. Your browser has asked the server to change protocols, and the server has complied.",
                '103': "Early hints. This returns some response headers before the rest of the server\'s response is ready.",
                '200': "Everything is OK. This is the code that is delivered when a web page or resource acts exactly the way it's expected to.",
                '201': "Created. The server has fulfilled the browser's request, and as a result, has created a new resource.",
                '202': "Accepted. The server has accepted your browser's request but is still processing it. The request ultimately may or may not result in a completed response.",
                '203': "Non-Authoritative Information. This status code may appear when a proxy is in use. It means that the proxy server received a 200 “Everything is OK” status code from the origin server, but has modified the response before passing it on to your browser.",
                '204': "No Content. This code means that the server has successfully processed the request, but is not going to return any content.",
                '205': "Reset Content. Like a 204 code, this means that how server has processed the request but is not going to return any content. However, it also requires that your browser resets the document view.",
                '206': "Partial Content. You may see this status code if your HTTP client (also known as your browser) uses 'range headers'. This enables your browser to resume paused downloads, as well as to split a download into multiple streams. A 206 code is sent when a range header causes the server to send only part of the requested resource.",
                '300': "Multiple Choices. Sometimes, there may be multiple possible resources the server can respond with to fulfill your browser's request. A 300 status code means that your browser now needs to choose between them. This may occur when there are multiple file type extensions available, or if the server is experiencing word sense disambiguation.",
                '301': "The requested resource has been moved permanently. This code is delivered when a web page or resource has been permanently replaced with a different resource. It is used for permanent URL redirection.",
                '302': "The requested resource has moved, but was found. This code is used to indicate that the requested resource was found, just not at the location where it was expected. It is used for temporary URL redirection.",
                '303': "See Other. Understanding a 303 status code requires that you know the difference between the four primary HTTP request methods. Essentially, a 303 code tells your browser that it found the resource your browser requested via POST, PUT, or DELETE. However, to retrieve it using GET, you need to make the appropriate request to a different URL than the one you previously used.",
                '304': "The requested resource has not been modified since the last time you accessed it. This code tells the browser that the resources stored in the browser cache haven't changed. It's used to speed up web page delivery by reusing previously-downloaded resources.",
                '307': "Temporary Redirect. This status code has replaced 302 “Found” as the appropriate action when a resource has been temporarily moved to a different URL. Unlike the 302 status code, it does not allow the HTTP method to change.",
                '308': "Permanent Redirect. The 308 status code is the successor to the 301 “Moved Permanently” code. It does not allow the HTTP method to change and indicates that the requested resource is now permanently located at a new URL.",
                '400': "Bad Request. The server can't return a response due to an error on the client's end. See our guide for resolving this error.",
                '401': "Unauthorized or Authorization Required. This is returned by the server when the target resource lacks valid authentication credentials. You might see this if you\'ve set up basic HTTP authentication using htpasswd.",
                '402': "Payment Required. Originally, this code was created for use as part of a digital cash system. However, that plan never followed through. Instead, it\'s used by a variety of platforms to indicate that a request cannot be fulfilled, usually due to a lack of required funds. Common instances include:",
                '403': "Access to that resource is forbidden. This code is returned when a user attempts to access something that they don't have permission to view. For example, trying to reach password-protected content without logging in might produce a 403 error.",
                '404': "The requested resource was not found. This is the most common error message of them all. This code means that the requested resource does not exist, and the server does not know if it ever existed.",
                '405': "Method not allowed. This is generated when the hosting server (origin server) supports the method received, but the target resource doesn't.",
                '406': "Not acceptable response. The requested resource is capable of generating only content that is not acceptable according to the accept headers sent in the request.",
                '407': "Proxy Authentication Required. A proxy server is in use and requires your browser to authenticate itself before continuing.",
                '408': "The server timed out waiting for the rest of the request from the browser. This code is generated when a server times out while waiting for the complete request from the browser. In other words, the server didn\'t get the full request that was sent by the browser. One possible cause could be net congestion resulting in the loss of data packets between the browser and the server.",
                '409': "Conflict. A 409 status code means that the server couldn't process your browser's request because there's a conflict with the relevant resource. This sometimes occurs due to multiple simultaneous edits.",
                '410': "The requested resource is gone and won't be coming back. This is similar to a 404 “Not Found” code, except a 410 indicates that the condition is expected and permanent.",
                '411': "Length Required. This means that the requested resource requires that the client specify a certain length and that it did not.",
                '412': "Precondition Failed. Your browser included certain conditions in its request headers, and the server did not meet those specifications.",
                '413': "Payload Too Large or 'Request Entity Too Large.' Your request is larger than the server is willing or able to process.",
                '414': "URI Too Long. This is usually the result of a GET request that has been encoded as a query string that is too large for the server to process.",
                '415': "Unsupported Media Type. The request includes a media type that the server or resource doesn't support.",
                '416': "Range Not Satisfiable. Your request was for a portion of a resource that the server is unable to return.",
                '417': "Expectation Failed. The server is unable to meet the requirements specified in the request's expect header field.",
                '418': "I'm a teapot. This code is returned by teapots that receive requests to brew coffee. It's also an April Fool's Joke from 1998.",
                '422': "Unprocessable Entity. The client request contains semantic errors, and the server can't process it.",
                '425': "Too Early. This code is sent when the server is unwilling to process a request because it may be replayed.",
                '426': "Upgrade Required. Due to the contents of the request's upgrade header field, the client should switch to a different protocol.",
                '428': "Precondition Required. The server requires conditions to be specified before processing the request.",
                '429': "Too many requests. This is generated by the server when the user has sent too many requests in a given amount of time (rate-limiting). This can sometimes occur due to bots or scripts attempting to access your site. In this case, you might want to try changing your WordPress login URL. You can also check out our guide to fixing a 429 “Too Many Requests” error.",
                '431': "Request Header Fields Too Large. The server can't process the request because the header fields are too large. This may indicate a problem with a single header field, or all of them collectively.",
                '451': "Unavailable for Legal Reasons. The operator of the server has received a demand to prohibit access to the resource you've requested (or a set of resources including the one you've requested). Fun fact: This code is a reference to Ray Bradbury's novel Fahrenheit 451.",
                '499': "Client closed request. This is returned by NGINX when the client closes the request while Nginx is still processing it.",
                '500': "There was an error on the server and the request could not be completed. This is generic code that simply means “internal server error”. Something went wrong on the server and the requested resource was not delivered. This code is typically generated by third-party plugins, faulty PHP, or even the connection to the database breaking. Check out our tutorials on how to fix the error establishing a database connection and other ways to resolve a 500 internal server error.",
                '501': "Not Implemented. This error indicates that the server does not support the functionality required to fulfill the request. This is almost always a problem on the web server itself, and usually must be resolved by the host. Check out our recommendations on how to resolve a 501 not implemented error.",
                '502': "Bad Gateway. This error code typically means that one server has received an invalid response from another, such as when a proxy server is in use. Other times a query or request will take too long, and so it is canceled or killed by the server and the connection to the database breaks. For more details, see our in-depth tutorial on how to fix the 502 Bad Gateway error.",
                '503': "The server is unavailable to handle this request right now. The request cannot be completed at this point in time. This code may be returned by an overloaded server that is unable to handle additional requests. We have a full guide on how to fix the 503 Service Unavailable Error.",
                '504': "The server, acting as a gateway, timed out waiting for another server to respond. This is the code returned when there are two servers involved in processing a request, and the first server times out waiting for the second server to respond. You can read more about how to fix 504 errors in our dedicated guide.",
                '505': "HTTP Version Not Supported. The server doesn't support the HTTP version the client used to make the request.",
                '508': "Resource Limit Is Reached limits on resources set by your web host have been reached. Check out our tutorial on how to resolve “508 Resource Limit Is Reached” error.",
                '509': "Bandwidth Limit Exceeded means your website is using more bandwidth than your hosting provider allows.",
                '511': "Network Authentication Required. This status code is sent when the network you\'re trying to use requires some form of authentication before sending your request to the server. For instance, you may need to agree to the Terms and Conditions of a public Wi-Fi hotspot.",
                '521': "Web server is down. Error 521 is a Cloudflare-specific error message. It means that your web browser was able to successfully connect to Cloudflare, but Cloudflare was not able to connect to the origin web server.",
                '525': "SSL Handshake Failed. Error 525 means that the SSL handshake between a domain using Cloudflare and the origin web server failed. If you are experiencing issues there are five methods you can try to easily fix error 525.",
                '222': 'This is a link to another Canvas Course.',
                '296': 'This is a Telephone Number',
                '297': 'This is a Sharepoint Link and is locked behind a login.',
                '298': 'This is an Email Link',
                '998': 'This is a broken/missing link that likely needs http:// to be replaced with https://',
                '999': "This is a Blackboard Link is either already broken or will stop working when Blackboard is taken down. Please fix asap."
                }
    
    return statusCode.get(code, "Unknown Error Code")

def getDescriptions(key):
    
    checkDescriptions = {
            'Module' : ['Module headings are consistent and logical', 'Page headings within modules are consistent and logical', 'Appropriate indenting has been used', 'Appropriate content has been published', 
                        'Logical sequence within migrated text (ie. limited repetitions, in-text headings are meaningful)', 'Page titles are consistent and logical'],
            'File Structure' : ['File structure is logical and supports the course approach presented within the module', 'Duplicate files need to be removed', 'Unused files are removed where appropriate', 'File names are consistent and logical', 'File names are meaningful'],
            'Assessments' : ['All assessment submission points have been made and are set up to a submission type', 'Points have been allocated to each submission point (where applicable)', 
                             'Assessment groups are weighted to total 100% and connect content relevant to the submission with the submission point'],
            'Link Information' : ['Links are included in an accessible format and working', 'Alot of 3XX errors are a product of old links that are http:// instead of https://.'],
            'Custom Fonts' : ['Fonts are consistent where possible', 'Content brought in directly from BB might have weird font tags'],
            'Course Images' : ['Images are included in an accessible format and working', 'Alot of 3XX errors are a product of old links that are http:// instead of https://'],
            'Unattached Pages' : ['Check superfluous and duplicate pages have been removed', 'Made sure all pages are linked to the appropriate module', 'Unneeded Pages are removed.'],
            'Placeholder' : ['Issues or incomplete content is addressed within the page (ie. placeholders are addressed, links are all configured correctly, attached items embedded appropriately)'],
            'Blackboard Terms' : ['Text should not mention removed technologies or terminologies (ie. Collaborate)'],
            'BB Echo Embed Code': ["This is from a course being mirgrated directly from BB, The embed code for Echo360's wont work in Canvas and will need to be replaced."],
            'File Link Information' : ['These are files that have been linked from sharepoint instead of the Canvas File structure, discuss with course convenor if this is the most sustainable way to manage these files within the course'],
            'Video Embed' : ['This is all the embedded content in your course.'],
            'Quizzes': ['TBD']
    }
    
    return checkDescriptions.get(key, "No Description")