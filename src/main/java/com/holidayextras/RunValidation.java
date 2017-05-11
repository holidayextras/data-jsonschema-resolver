package com.holidayextras;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.networknt.schema.JsonSchema;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.ValidationMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Set;

/**
 * Hello world!
 *
 */
public class RunValidation
{
    Logger LOG = LoggerFactory.getLogger(RunValidation.class);

    public static JsonNode getJsonNodeFromUrl(String url)  throws MalformedURLException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode node = null;
        try {
            node = mapper.readTree(new URL(url));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return node;
    }

    public static JsonSchema getJsonSchemaFromUrl(String url) throws MalformedURLException {
        JsonSchemaFactory factory = new JsonSchemaFactory();
        JsonSchema schema = factory.getSchema(new URL(url));
        return schema;
    }


    public static String EXAMPLE_BASE = "http://127.0.0.1:12346/examples/";
    public static String SCHEMA_BASE = "http://127.0.0.1:12345/";

    public static void checkSchema(String id) throws MalformedURLException {

        String exampleUrl = EXAMPLE_BASE + id + "/" + id + ".json";
        String schemaUrl = SCHEMA_BASE + id + "/schema-" + id + ".json";

        JsonNode example = RunValidation.getJsonNodeFromUrl(exampleUrl);
        JsonSchema schema = RunValidation.getJsonSchemaFromUrl(schemaUrl);

        Set<ValidationMessage> errors = schema.validate(example);

        System.out.println("Validating " + id);
        for (ValidationMessage message : errors) {
            System.out.println(message.toString());
        }
        System.out.println(id + " validated");
    }


    public static void main( String[] args ) throws Exception
    {
        try {

            System.out.println("Hello World!");
            JsonNode node = RunValidation.getJsonNodeFromUrl("http://127.0.0.1:12346/examples/b/b.json");
            System.out.println("Node:");
            System.out.println(node);

            JsonNode schemaNode = RunValidation.getJsonNodeFromUrl("http://127.0.0.1:12345/b/schema-b.json");
            System.out.println("Schema Node:");
            System.out.println(schemaNode);

            System.out.println("Loading Referenced Schema:");
            JsonSchema schema = RunValidation.getJsonSchemaFromUrl("http://127.0.0.1:12345/b/schema-b.json");
            System.out.println("Schema");
            System.out.println(schema);

            String [] ids = {"a", "b", "c"};

            for (String id : ids) {
                RunValidation.checkSchema(id);
            }

        } catch (MalformedURLException e) {

            System.out.println(e.getStackTrace());
            System.out.println("Yikes!");

        }
    }
}
