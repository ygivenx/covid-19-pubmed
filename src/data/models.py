from sqlalchemy import Integer, ForeignKey, String, Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Metadata(Base):
    __tablename__ = 'metadata'
    cord_uid = Column(String)
    paper_key = Column(String, primary_key=True)
    sha = Column(String)
    source_x = Column(String)
    title = Column(String)
    doi = Column(String)
    pmcid = Column(String)
    pubmed_id = Column(String)
    license = Column(String)
    abstract = Column(String)
    publish_time = DateTime(String)
    authors = Column(String)
    journal = Column(String)
    microsoft_academic_paper_id = Column("Microsoft Academic Paper ID", String)
    who_covidence = Column("WHO #Covidence", String)
    has_pdf_parse = Column(Boolean)
    has_pmc_xml_parse = Column(Boolean)
    full_text_file = Column(String)
    url = Column(String)
