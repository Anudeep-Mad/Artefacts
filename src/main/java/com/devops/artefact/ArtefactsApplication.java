package com.devops.artefact;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan
public class ArtefactsApplication {

	public static void main(String[] args) {
		SpringApplication.run(ArtefactsApplication.class, args);
	}
}
