package edu.utk.gsda;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpStatus;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.StringRequestEntity;

public class CalaisHttpClient
{
		private final String CALAIS_URL = "https://api.thomsonreuters.com/permid/calais"; //"http://api.opencalais.com/tag/rs/enrich";
	    private HttpClient client;
	    private PostMethod method;
	    
	    public void initMethod()
	    {
	    		
	    		method = new PostMethod(CALAIS_URL);

	            // Set mandatory parameters
	           // method.setRequestHeader("x-calais-licenseID", "gffvtc7epu3tn7xkyrhbtdvk");
	    		method.setRequestHeader("x-ag-access-token", "5CSCGy1jw4x7vY0FtLERrHZHDaRwynKq");
	    		
	            // Set input content type
	            method.setRequestHeader("Content-Type", "TEXT/RAW; charset=UTF-8");
	            //method.setRequestHeader("Content-Type", "text/html; charset=UTF-8");
	            //method.setRequestHeader("Content-Type", "text/raw; charset=UTF-8");
	            method.setRequestHeader("omitOutputtingOriginalText", "true");
	            

	    		// Set response/output format
	           // method.setRequestHeader("Accept", "text/simple");
	            method.setRequestHeader("outputFormat", "application/json");

	            // Enable Social Tags processing
	           // method.setRequestHeader("enableMetadataType", "SocialTags");
	            method.setRequestHeader("x-calais-selectiveTags", "socialtags");
	            
	    }
	    
	    public String getAnnotatedResult(String originString)
	    {
	    		try
				{
	    				client = new HttpClient();
	    	            client.getParams().setParameter("http.useragent", "Calais Rest Client");
	    	            
	    	            initMethod();
	    				
	    				method.setRequestEntity(new StringRequestEntity(originString, null,null));
	    				int returnCode = client.executeMethod(method);
	    				
	    				if (returnCode == HttpStatus.SC_OK) 
	    	            {
	    						BufferedReader reader = new BufferedReader(new InputStreamReader(method.getResponseBodyAsStream(), "UTF-8"));    					       
	    					    
	    						StringBuffer stringBuffer = new StringBuffer();
	    						String line;
					            while ((line = reader.readLine()) != null) 
					            {
					                stringBuffer.append(line);
					            } 
	    					    
					            reader.close();
					            return stringBuffer.toString();
	    	            }
	    				else
	    				{
	    	                System.err.println("request failed: " );
	    	                System.err.println("Got code: " + returnCode);
	    	                return null;
	    				}
	    			
	    				
				}
	    		catch (Exception e)
				{
						e.printStackTrace();
				}
	    		
	    		return null;
	    		
	    }
	    

}
