package JavaExtractor.Common;

import java.util.ArrayList;
import com.github.javaparser.ast.Node;

public class MethodContent {
	private ArrayList<Node> leaves;
	private String name;
	private long length;
	private String description;

	public MethodContent(ArrayList<Node> leaves, String name, long length) {
		this.leaves = leaves;
		this.name = name;
		this.length = length;
	}
	
	public MethodContent(ArrayList<Node> leaves, String name, long length, String description) {
		this(leaves, name, length);
		this.description = description;
	}

	public ArrayList<Node> getLeaves() {
		return leaves;
	}

	public String getName() {
		return name;
	}

	public long getLength() {
		return length;
	}

	public String getDescription() {
		return description;
	}
}
