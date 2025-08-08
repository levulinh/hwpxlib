package kr.dogfoot.hwpxlib.reader.masterpage_xml;

import kr.dogfoot.hwpxlib.commonstrings.AttributeNames;
import kr.dogfoot.hwpxlib.commonstrings.ElementNames;
import kr.dogfoot.hwpxlib.object.common.HWPXObject;
import kr.dogfoot.hwpxlib.object.common.SwitchableObject;
import kr.dogfoot.hwpxlib.object.content.masterpage_xml.MasterPageXMLFile;
import kr.dogfoot.hwpxlib.object.content.masterpage_xml.enumtype.MasterPageType;
import kr.dogfoot.hwpxlib.object.content.section_xml.SubList;
import kr.dogfoot.hwpxlib.reader.common.ElementReader;
import kr.dogfoot.hwpxlib.reader.common.ElementReaderSort;
import kr.dogfoot.hwpxlib.reader.section_xml.SubListReader;
import kr.dogfoot.hwpxlib.reader.util.ValueConvertor;
import org.xml.sax.Attributes;

public class MasterPageFileReader extends ElementReader {
    private MasterPageXMLFile masterPageXMLFile;

    @Override
    public ElementReaderSort sort() {
        return ElementReaderSort.MasterPageFile;
    }

    public void masterPageXMLFile(MasterPageXMLFile masterPageXMLFile) {
        this.masterPageXMLFile = masterPageXMLFile;
    }

    @Override
    protected void setAttribute(String name, String value) {
        switch (name) {
            case AttributeNames.id:
                masterPageXMLFile.id(value);
                break;
            case AttributeNames.type:
                masterPageXMLFile.type(MasterPageType.fromString(value));
                break;
            case AttributeNames.pageNumber:
                masterPageXMLFile.pageNumber(ValueConvertor.toInteger(value));
                break;
            case AttributeNames.pageDuplicate:
                masterPageXMLFile.pageDuplicate(ValueConvertor.toBoolean(value));
                break;
            case AttributeNames.pageFront:
                masterPageXMLFile.pageFront(ValueConvertor.toBoolean(value));
                break;
        }
    }

    @Override
    public void childElement(String name, Attributes attrs) {
        switch (name) {
            case ElementNames.hp_subList:
                masterPageXMLFile.createSubList();
                subList(masterPageXMLFile.subList(), name, attrs);
                break;
        }
    }

    @Override
    public HWPXObject childElementInSwitch(String name, Attributes attrs) {
        switch (name) {
            case ElementNames.hp_subList:
                SubList subList = new SubList();
                subList(subList, name, attrs);
                return subList;
        }
        return null;
    }

    private void subList(SubList subList, String name, Attributes attrs) {
        ((SubListReader) xmlFileReader().setCurrentElementReader(ElementReaderSort.SubList))
                .subList(subList);

        xmlFileReader().startElement(name, attrs);
    }

    @Override
    public SwitchableObject switchableObject() {
        return masterPageXMLFile;
    }
}
