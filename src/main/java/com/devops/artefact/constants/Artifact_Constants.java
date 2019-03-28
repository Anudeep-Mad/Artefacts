package com.devops.artefact.constants;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class Artifact_Constants {

	public static final List<String> env_var_cd_ci = Collections.unmodifiableList(new ArrayList<String>() {/**
	 * 
	 */
		private static final long serialVersionUID = 1L;

		{
			add("test11");
			add("uat");
		}});
	public static final List<String> env_var = Collections.unmodifiableList(new ArrayList<String>() {/**
		 * 
		 */
			private static final long serialVersionUID = 1L;

			{
				add("cstg");
				add("dev15");
				add("lt");
				add("stage");
				add("test12");
				add("test14");
				add("test15");
				add("test31");
				add("test36");
				add("test41");
				add("test50");
				add("uat2");
			}});

	public static final List<String> env_type = Collections.unmodifiableList(new ArrayList<String>(){

		private static final long serialVersionUID = 2L;
		{
			add("Non CD/CI");
			add("CD/CI");
		}

	});



}
