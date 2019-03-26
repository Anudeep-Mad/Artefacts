package com.devops.artefact.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.servlet.http.HttpServletResponse;

import org.apache.tomcat.util.http.fileupload.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.devops.artefact.constants.Artifact_Constants;
import com.devops.artefact.model.EnvModel;
import com.devops.artefact.service.ArtifactService;


@Controller
public class ArtefactController {
	
	@Autowired
	public ArtifactService artifactService;
	 
	@RequestMapping("/")
	public String index(Model model) {
		model.addAttribute("envModel",new EnvModel());
		model.addAttribute("env_var",Artifact_Constants.env_var);
		return "home";
	}
	
	/*@PostMapping(value="/welcome")
	public String welcome(@ModelAttribute("envModel") EnvModel envModel) throws IOException {
		return artifactService.Compare(envModel);
	}*/
	@PostMapping(value="/welcome")
	public void welcome(@ModelAttribute("envModel") EnvModel envModel,HttpServletResponse response) throws IOException {
		String current_ts = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new Date(System.currentTimeMillis()));
		File file = new File("/home/amedishetti/Artifact_Comparator/sp/compare_"+current_ts+".txt");
		artifactService.Compare_2(envModel,"/home/amedishetti/Artifact_Comparator/sp/compare_"+current_ts+".txt" );
		//return ResponseEntity.ok().header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + file.getName() + "\"").body(file);
		response.addHeader("Content-disposition", "attachment;filename=compare_"+current_ts+".txt");
		response.setContentType("application/pdf");
		InputStream myStream =new FileInputStream(file);
		//InputStream myStream = new BufferedInputStream(new FileInputStream(file));
		// Copy the stream to the response's output stream.
		IOUtils.copy(myStream, response.getOutputStream());
		response.flushBuffer();
	}
	
	
	@PostMapping(value="/compareByDates")
	@ResponseBody
	public String validateDeployment(@RequestBody EnvModel envModel) throws IOException {
		return artifactService.Compare(envModel);
	}
	
	@PostMapping(value="/compareByUserStory")
	@ResponseBody
	public String validateDeploymentByUserStory(@RequestBody EnvModel envModel) throws IOException {
		return artifactService.Compare(envModel);
	}
	
	@PostMapping(value="/compareForFile")
	@ResponseBody
	public void sendCompFile(@RequestBody EnvModel envModel, HttpServletResponse response) throws IOException {
		String current_ts = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new Date(System.currentTimeMillis()));
		File file = new File("/home/amedishetti/Artifact_Comparator/sp/compare_"+current_ts+".txt");
		artifactService.Compare_2(envModel,"/home/amedishetti/Artifact_Comparator/sp/compare_"+current_ts+".txt" );
		//return ResponseEntity.ok().header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + file.getName() + "\"").body(file);
		response.addHeader("Content-disposition", "attachment;filename=compare_"+current_ts+".txt");
		response.setContentType("application/pdf");
		InputStream myStream =new FileInputStream(file);
		//InputStream myStream = new BufferedInputStream(new FileInputStream(file));
		// Copy the stream to the response's output stream.
		IOUtils.copy(myStream, response.getOutputStream());
		response.flushBuffer();
	}

}
