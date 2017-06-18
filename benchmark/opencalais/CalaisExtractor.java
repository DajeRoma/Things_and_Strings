package edu.utk.gsda;

import java.util.Hashtable;
import java.util.Vector;

import org.json.JSONArray;
import org.json.JSONObject;
//import org.tartarus.snowball.SnowballStemmer;

public class CalaisExtractor
{	
		private CalaisHttpClient calaisHttpClient = null;
		
		public CalaisExtractor()
		{
				calaisHttpClient = new CalaisHttpClient();
		}
		
		public Vector<String> extractEntities(String originString)
		{
				/*String licenseID = "gffvtc7epu3tn7xkyrhbtdvk";
				String content = originString ;
				String paramsXML = "<c:params xmlns:c=\"http://s.opencalais.com/1/pred/\" xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"> "+
															"<c:processingDirectives c:contentType=\"TEXT/RAW\" c:enableMetadataType=\"GenericRelations, SocialTags\" c:outputFormat=\"text/simple\"></c:processingDirectives> "+
															"<c:userDirectives c:allowDistribution=\"true\" c:allowSearch=\"true\" c:externalID=\"17cabs901\" c:submitter=\"ABC\"></c:userDirectives> "+
															"<c:externalMetadata></c:externalMetadata></c:params>";
				*/
				try
				{
						String output = calaisHttpClient.getAnnotatedResult(originString);//new CalaisLocator().getcalaisSoap().enlighten(licenseID, content, paramsXML);
						
						System.out.println(output);
						
						JSONObject resultJsonObject = new JSONObject(output);
						String docID = resultJsonObject.getJSONObject("doc").getJSONObject("info").getString("docId");
						
						Vector<String> entitiesVector = new Vector<>();
						
						int  socialTagIndex = 0;
						while(true)
						{
							socialTagIndex++;
							JSONObject socialTagObject = null;
							
							try 
							{
								socialTagObject = resultJsonObject.getJSONObject(docID+"/SocialTag/"+socialTagIndex);
							} 
							catch (Exception e) 
							{
								// TODO: handle exception
							}
							
							if(socialTagObject ==  null)
								break;
							
							String entityString = socialTagObject.getString("name");
							entityString = entityString.toLowerCase();
							
							int commaIndex = entityString.indexOf(",");
							if(commaIndex != -1)
								entityString = entityString.substring(0, commaIndex).trim();
							
							entitiesVector.add(entityString);
						}
						
						return entitiesVector;
						
						/*int index1 = output.indexOf("-->");
					    output = output.substring(index1+4);
					    int index2 = output.indexOf("-->");
					    if(index2 == -1)
					    {
					    		 JSONObject resultObject = new JSONObject();
								    resultObject.put("geo", new JSONArray());
								    resultObject.put("thematic", new JSONArray());
								    //resultObject.put("type", new JSONArray());
								    
								    return resultObject;
					    }
					    
					    output = output.substring(3,index2-1);
					    
					   // System.out.println(output);
					    String[] terms = output.split(",");
					    
					   // Class stemClass = Class.forName("org.tartarus.snowball.ext.englishStemmer");
				      //  SnowballStemmer stemmer = (SnowballStemmer) stemClass.newInstance();
				        
				        JSONArray geoTermArray = new JSONArray();
				        JSONArray thematicTermArray = new JSONArray();
				        JSONArray typesArray = new JSONArray();
					    
				        Hashtable<String, Object> existingTable = new Hashtable<String, Object>();
					    for(int i=0;i<terms.length;i++)
					    {
					    		String thisTerm = terms[i];
					    		String[] termResult = thisTerm.split(":");
					    		
					    		String termType = termResult[0].trim();
					    		String termName = termResult[1].trim();
					    		
					    		if(termType.equals("City") || termType.equals("ProvinceOrState") || termType.equals("Country") ||  termType.equals("Place") ||    termType.equals("Continent"))
					    		{
					    				geoTermArray.put(termName.toLowerCase());
					    		}
					    		else
					    		{

					    				//stemmer.setCurrent(termName);
							    	//	stemmer.stem();
							    	//	termName = stemmer.getCurrent();
							    	//	termName = termName.toLowerCase();
							    		
							    		if(existingTable.containsKey(termName)) continue;
							    		existingTable.put(termName, new Object());
							    		
							    		if(termName.split(" ").length<=3)
							    				thematicTermArray.put(termName);
								}
					    		
					    		
					    		
					    	
					    	
					    		
					    		//typesArray.put(termType);
					    }
					    
					    JSONObject resultObject = new JSONObject();
					    resultObject.put("geo", geoTermArray);
					    resultObject.put("thematic", thematicTermArray);
					    //resultObject.put("type", typesArray);
					    
					    return resultObject;
					    
					    //System.out.println(terms[0]);
*/					   
						
				} 
				catch (Exception e)
				{
						e.printStackTrace();
				} 
				
			/*	try
				{
						JSONObject resultObject = new JSONObject();
					    resultObject.put("geo", new JSONArray());
					    resultObject.put("thematic", new JSONArray());
					    resultObject.put("type", new JSONArray());
					    
					    return resultObject;
				} 
				catch (Exception e)
				{
						e.printStackTrace();
				}*/
				
				return null;
				
				
		}
		

}
