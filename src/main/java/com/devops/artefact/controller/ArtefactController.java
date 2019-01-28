package com.devops.artefact.controller;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.devops.artefact.model.EnvModel;
import com.devops.artefact.service.ArtifactService;


@Controller
public class ArtefactController {
	
	@Autowired
	public ArtifactService artifactService;
	 
	@RequestMapping("/")
	public String index(Model model) {
		model.addAttribute("envModel",new EnvModel());
		return "home";
	}
	
	@PostMapping(value="/welcome")
	public String welcome(@ModelAttribute("envModel") EnvModel envModel) throws IOException {
		return artifactService.Compare(envModel);
	}
	
	@PostMapping(value="/compare")
	@ResponseBody
	public String validateDeployment(@RequestBody EnvModel envModel) throws IOException {
		return artifactService.Compare(envModel);
	}

}
