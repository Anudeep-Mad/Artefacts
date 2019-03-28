package com.devops.artefact.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Component;

import com.devops.artefact.model.EnvModel;

@Component
public class ArtifactService {

	String s = null,command;
	public String Compare(EnvModel envModel) throws IOException {
		if(envModel.getSelection_type().equals("date")) {
		command="python3.4 " + "final_last.py " + envModel.getEnv_name()+" "+ envModel.getFromdate()+" "+envModel.getTodate()+" "+envModel.getEmail();
		}
		else if(envModel.getSelection_type().equals("us"))
				command="python3.4 " + "user_story.py " + envModel.getEnv_name()+" "+envModel.getUser_story()+" "+envModel.getEmail();
		
		System.out.println(command);
		Process p = Runtime.getRuntime().exec(command);
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
	
	public void Compare_2(EnvModel envModel, String file_name) throws IOException {
		if(envModel.getSelection_type().equals("date")) {
			if(envModel.getEnv_type().equals("Non-CD/CI"))
				command="python3.4 " + "artifact_comparator.py " + envModel.getEnv_name()+" "+envModel.getEnv_type()+" "+ file_name +" "+ envModel.getFromdate()+" "+envModel.getTodate()+" "+envModel.getEmail();
			else
				command="python3.4 " + "artifact_comparator.py " + envModel.getEnv_name_cd_ci()+" "+envModel.getEnv_type()+" "+ file_name +" "+ envModel.getFromdate()+" "+envModel.getTodate()+" "+envModel.getEmail();
			}
			else if(envModel.getSelection_type().equals("us"))
					command="python3.4 " + "user_story.py " + envModel.getEnv_name()+" "+ file_name +" "+envModel.getUser_story()+" "+envModel.getEmail();
			
			System.out.println(command);
			Process p = Runtime.getRuntime().exec(command);
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
	}


}
