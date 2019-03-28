package com.devops.artefact.model;

public class EnvModel {
	

	private String selection_type,env_name_cd_ci, env_name,fromdate,todate,user_story,email,env_type;

	public String getEnv_name_cd_ci() {
		return env_name_cd_ci;
	}

	public void setEnv_name_cd_ci(String env_name_cd_ci) {
		this.env_name_cd_ci = env_name_cd_ci;
	}

	public String getEnv_type() {
		return env_type;
	}

	public void setEnv_type(String env_type) {
		this.env_type = env_type;
	}

	public String getUser_story() {
		return user_story;
	}

	public void setUser_story(String user_story) {
		this.user_story = user_story;
	}

	public String getEnv_name() {
		return env_name;
	}

	public void setEnv_name(String env_name) {
		this.env_name = env_name;
	}

	public String getFromdate() {
		return fromdate;
	}

	public void setFromdate(String fromdate) {
		this.fromdate = fromdate;
	}

	public String getTodate() {
		return todate;
	}

	public void setTodate(String todate) {
		this.todate = todate;
	}

	public String getSelection_type() {
		return selection_type;
	}

	public void setSelection_type(String selection_type) {
		this.selection_type = selection_type;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	

}
