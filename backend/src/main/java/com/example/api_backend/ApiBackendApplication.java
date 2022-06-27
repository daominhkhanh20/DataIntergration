package com.example.api_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@SpringBootApplication
public class ApiBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiBackendApplication.class, args);
                 //-Djdk.tls.client.protocols=TLSv1.2
	}

}
