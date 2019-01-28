package com.devops.artefact.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Component;

import com.devops.artefact.model.EnvModel;

@Component
public class ArtifactService {

	String s = null;
	public String Compare(EnvModel envModel) throws IOException {
		//Process p = Runtime.getRuntime().exec("py " + "C:\\Users\\amedishetti\\Documents\\Anudeep\\AI\\python_AI\\Artifact\\code\\code_updated.py \"Inf Shell Files\" " + envModel.getEnv_name()+" "+ envModel.getFromdate()+" "+envModel.getTodate()+" "+envModel.getEmail());
		Process p = Runtime.getRuntime().exec("python3.4 " + "cent_comp.py \"Inf Shell Files\" " + envModel.getEnv_name()+" "+ envModel.getFromdate()+" "+envModel.getTodate()+" "+envModel.getEmail());
		BufferedReader stdInput = new BufferedReader(new 
				InputStreamReader(p.getInputStream()));

		BufferedReader stdError = new BufferedReader(new 
				InputStreamReader(p.getErrorStream()));

		// read the output from the command
		System.out.println("Here is the standard output of the command:\n");
		while ((s = stdInput.readLine()) != null) {
			System.out.println(s);
		}

		// read any errors from the attempted command
		System.out.println("Here is the standard error of the command (if any):\n");
		while ((s = stdError.readLine()) != null) {
			System.out.println(s);
		}
		return "index";
	}


}
