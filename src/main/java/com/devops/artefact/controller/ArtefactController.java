package com.devops.artefact.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.devops.artefact.model.EnvModel;


@Controller
public class ArtefactController {
	 String s = null;
	 
	@RequestMapping("/")
	public String index(Model model) {
		model.addAttribute("envModel",new EnvModel());
		return "home";
	}
	
	@PostMapping(value="/welcome")
	public String welcome(@ModelAttribute("envModel") EnvModel envModel) throws IOException {
		System.out.println(envModel.getEnv_name());
		Process p = Runtime.getRuntime().exec("py " + "C:\\Users\\amedishetti\\Documents\\Anudeep\\AI\\python_AI\\Artifact\\code\\code_updated.py \"Inf Shell Files\" " + envModel.getEnv_name()+" "+ envModel.getFromdate()+" "+envModel.getTodate()+" "+envModel.getEmail());
		//String fetching = "py " + "C:\\Users\\amedishetti\\Documents\\Anudeep\\AI\\python_AI\\Artifact\\mysql_connect.py " + envModel.getEnv_name() + "";
		//String[] commandToExecute = new String[]{"cmd.exe", "/c", fetching};
		//Runtime.getRuntime().exec(commandToExecute);
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
