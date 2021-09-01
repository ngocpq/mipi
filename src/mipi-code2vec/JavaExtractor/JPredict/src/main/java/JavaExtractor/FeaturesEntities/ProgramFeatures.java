package JavaExtractor.FeaturesEntities;

import java.util.ArrayList;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonIgnore;

public class ProgramFeatures {
	private String name;
	private String description;

	private ArrayList<ProgramRelation> features = new ArrayList<>();

	public ProgramFeatures(String name) {
		this.name = name;
	}
	
	public ProgramFeatures(String name, String description) {
		this(name);
		this.description = description;
	}

	@SuppressWarnings("StringBufferReplaceableByString")
	@Override
	public String toString() {
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.append(name).append(" ");
		stringBuilder.append(features.stream().map(ProgramRelation::toString).collect(Collectors.joining(" ")));

		return stringBuilder.toString();
	}
	
	public String toString(boolean printDescription) {
		if (!printDescription)
			return this.toString();
		
		StringBuilder stringBuilder = new StringBuilder();
		String desc = "";
		if(this.description!=null) {
			desc = this.description.replace("|", "||").replace(" ", "|");					
		}				
		stringBuilder.append(name).append("@").append(desc).append(" ");
		stringBuilder.append(features.stream().map(ProgramRelation::toString).collect(Collectors.joining(" ")));

		return stringBuilder.toString();
	}
	
	public void addFeature(Property source, String path, Property target) {
		ProgramRelation newRelation = new ProgramRelation(source, target, path);
		features.add(newRelation);
	}

	@JsonIgnore
	public boolean isEmpty() {
		return features.isEmpty();
	}

	public void deleteAllPaths() {
		features.clear();
	}

	public String getName() {
		return name;
	}
	
	public String getDescription() {
		return description;
	}

	public ArrayList<ProgramRelation> getFeatures() {
		return features;
	}

}
